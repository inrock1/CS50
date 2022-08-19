from cs50 import SQL
from flask import Flask, flash, redirect, jsonify, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Настроика приложения
app = Flask(__name__)

# Убедитесь, что шаблоны автоматически перезагружаются
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Убедитесь, что ответы не кэшируются
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Пользовательский фильтр
app.jinja_env.filters["usd"] = usd

# Настроить сеанс для использования файловой системы (вместо подписанных файлов cookie)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Настройте библиотеку CS50 для использования базы данных SQLite
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # поиск текущего пользователя
    users = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])
    quotes = {}

    for stock in stocks:
        quotes[stock["symbol"]] = lookup(stock["symbol"])

    cash_remaining = users[0]["cash"]
    total = cash_remaining
# рендер страницы index.html
    return render_template("index.html", quotes=quotes, stocks=stocks, total=total, cash_remaining=cash_remaining)


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
# получаем список всех найденых username
    username = request.args.get("username")
# если длина введённого username <1 - ошибка
    if len(username) < 1:
        return jsonify(False)
# ищем в бд username и выводим в json
    check_username = db.execute(
        "SELECT username FROM users WHERE username = :un", un=username)
#сли совпадений нет - true
    if len(check_username) == 0:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        # Проверьте, существует ли символ
        if quote == None:
            return apology("invalid symbol", 400)

        # Проверьте, было ли в акциях положительное целое число
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 400)

        # Проверьте, не было ли запрошено 0 акций
        if shares <= 0:
            return apology("can't buy less than or 0 shares", 400)

        # запрос БД для имени пользователя
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # Сколько средств пользователь еще имеет в своем аккаунте
        cash_remaining = rows[0]["cash"]
        price_per_share = quote["price"]

        # Рассчитать цену запрашиваемых акций
        total_price = price_per_share * shares
# Если средств недостаточно, выводим сообщение и форму увеличения доступных средств
        if total_price > cash_remaining:
            flash("Not enough funds!")
            return render_template("add_funds.html")
        # запись транзакции в БД
        db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price_per_share) VALUES(:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"],
                   symbol=request.form.get("symbol"),
                   shares=shares,
                   price=price_per_share)

        flash("Bought!")

        return redirect(url_for("index"))

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
 # запрос в БД данные пользователя
    transactions = db.execute(
        "SELECT symbol, shares, price_per_share, created_at FROM transactions WHERE user_id = :user_id ORDER BY created_at ASC", user_id=session["user_id"])
# рендер history.html
    return render_template("history.html", transactions=transactions)


 # Этот блок реализован в шаблоне задания
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect(url_for("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for("index"))


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow user to change her password"""

    if request.method == "POST":

        # Убедитесь, что текущий пароль не пуст
        if not request.form.get("current_password"):
            return apology("must provide current password", 400)

        # Запрос БД для user_id
        rows = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # Убедитесь, что текущий пароль правильный
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("current_password")):
            return apology("invalid password", 400)

        # Убедитесь, что новый пароль не пуст
        if not request.form.get("new_password"):
            return apology("must provide new password", 400)

        # Убедитесь, что подтверждение нового пароля не пусто
        elif not request.form.get("new_password_confirmation"):
            return apology("must provide new password confirmation", 400)

        # Убедитесь, что новый пароль и подтверждение совпадают
        elif request.form.get("new_password") != request.form.get("new_password_confirmation"):
            return apology("new password and confirmation must match", 400)

        # Обновить database
        hash = generate_password_hash(request.form.get("new_password"))
        rows = db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", user_id=session["user_id"], hash=hash)

        # Показать сообщение
        flash("Changed!")

    return render_template("change_password.html")



@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", quote=quote)


    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Убедитесь, что пользователь ввел имя
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Убедитесь, что пользователь ввел пароль
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Убедитесь, что  password and confirmation совпадают
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # хэшируйте пароль и вставьте нового пользователя в базу данных
        hash = generate_password_hash(request.form.get("password"))
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                                 username=request.form.get("username"),
                                 hash=hash)

        # проверка уникальности username
        if not new_user_id:
            return apology("username taken", 400)

        # Запомнить, какой пользователь вошел в систему
        session["user_id"] = new_user_id

        # ПОказать сообщение
        flash("Registered!")

        # Перенаправить пользователя на home page
        return redirect(url_for("index"))

    # Если пользователь кликнулна ссылку
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        # Проверьте, существует ли символ
        if quote == None:
            return apology("invalid symbol", 400)

        # Проверьте, было ли в акциях положительное целое число
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 400)

        # Проверьте, не было ли запрошено <=0 акций
        if shares <= 0:
            return apology("can't sell less than or 0 shares", 400)

        # Проверьте, достаточно ли у пользователя акций
        stock = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id AND symbol = :symbol GROUP BY symbol",
                           user_id=session["user_id"], symbol=request.form.get("symbol"))

        if len(stock) != 1 or stock[0]["total_shares"] <= 0 or stock[0]["total_shares"] < shares:
            return apology("you can't sell less than 0 or more than you own", 400)

        # Запрос к database для username
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # Сколько средств пользователь еще имеет в своем аккаунте
        cash_remaining = rows[0]["cash"]
        price_per_share = quote["price"]

        # Рассчитать цену запрашиваемых акций
        total_price = price_per_share * shares

        # Запись в БД, transaction
        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price_per_share) VALUES(:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"],
                   symbol=request.form.get("symbol"),
                   shares=-shares,
                   price=price_per_share)

        flash("Sold!")

        return redirect(url_for("index"))

    else:
        stocks = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])

        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# слушатель ошибок
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)