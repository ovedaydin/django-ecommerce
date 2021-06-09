var vanillaCalendar = {
  month: document.querySelectorAll('[data-calendar-area="month"]')[0],
  next: document.querySelectorAll('[data-calendar-toggle="next"]')[0],
  previous: document.querySelectorAll('[data-calendar-toggle="previous"]')[0],
  label: document.querySelectorAll('[data-calendar-label="month"]')[0],
  activeDates: null,
  date: new Date(),
  todaysDate: new Date(),

  init: function (options) {
    this.options = options;
    this.date.setDate(1);
    this.createMonth();
    this.createListeners();
  },

  createListeners: function () {
    var _this = this;
    this.next.addEventListener("click", function () {
      _this.clearCalendar();
      var nextMonth = _this.date.getMonth() + 1;
      _this.date.setMonth(nextMonth);
      _this.createMonth();
    });
    // Clears the calendar and shows the previous month
    this.previous.addEventListener("click", function () {
      _this.clearCalendar();
      var prevMonth = _this.date.getMonth() - 1;
      _this.date.setMonth(prevMonth);
      _this.createMonth();
    });
  },

  createDay: function (num, day, year) {
    var newDay = document.createElement("div");
    var dateEl = document.createElement("span");

    var freeShipping = document.createElement("span");
    if (this.options.shippingCost !== "0.00") {
      if (this.options.discount !== "0.00") {
        freeShipping.innerText = "indirimli";
      } else {
        freeShipping.innerText = "ücretsiz";
      }
    }

    freeShipping.classList.add("freeshipping");
    dateEl.innerHTML = num;
    newDay.className = "vcal-date";

    newDay.setAttribute("data-calendar-date", this.date);

    // if it's the first day of the month
    if (num === 1) {
      if (day === 0) {
        newDay.style.marginLeft = 6 * 14.28 + "%";
      } else {
        newDay.style.marginLeft = (day - 1) * 14.28 + "%";
      }
    }

    if (
      this.options.disablePastDays &&
      this.date.getTime() <= this.todaysDate.getTime()
    ) {
      // if you add -1 you can pick today as well, but we want to pick tomorrow at least
      newDay.classList.add("vcal-date--disabled");
    } else {
      newDay.classList.add("vcal-date--active");
      newDay.setAttribute("data-calendar-status", "active");
      if (this.date.getDay() === 6) {
        newDay.appendChild(freeShipping);
      }
    }

    if (this.date.toString() === this.todaysDate.toString()) {
      newDay.classList.add("vcal-date--today");
    }

    newDay.appendChild(dateEl);

    this.month.appendChild(newDay);
  },

  dateClicked: function () {
    var _this = this;
    this.activeDates = document.querySelectorAll(
      '[data-calendar-status="active"]'
    );
    for (var i = 0; i < this.activeDates.length; i++) {
      this.activeDates[i].addEventListener("click", function (event) {
        var picked = document.querySelectorAll(
          '[data-calendar-label="picked"]'
        )[0];
        picked.innerHTML = this.dataset.calendarDate;
        date = new Date(this.dataset.calendarDate);
        year = date.getFullYear();
        month = date.getMonth()+1;
        dt = date.getDate();

        if (dt < 10) {
          dt = '0' + dt;
        }
        if (month < 10) {
          month = '0' + month;
        }

        var dateControl = document.querySelector('input[type="date"]');
        dateControl.value = year+'-' + month + '-'+dt;
        document.getElementById("picked").innerText= dateControl.value;

        _this.removeActiveClass();
        this.classList.add("vcal-date--selected");
        var thatday =
          this.dataset.calendarDate[0] + this.dataset.calendarDate[1]; //first two letters of a day
        if (thatday === "Sa") {
          for (var i = 0; i < _this.options.biggestAmounts.length; i++) {
            _this.options.biggestAmounts[i].innerText =
              _this.options.withoutShipping;
          }
          for (var i = 0; i < _this.options.prices.length; i++) {
            _this.options.prices[i].innerText = _this.options.withoutShipping;
          }
          for (var i = 0; i < _this.options.shippingFees.length; i++) {
            _this.options.shippingFees[i].innerText =
              _this.options.discount + " TL";
          }
          document.getElementById("shipping_cost").value = _this.options.discount;
        } else {
          for (var i = 0; i < _this.options.biggestAmounts.length; i++) {
            _this.options.biggestAmounts[i].innerText =
              _this.options.withShipping;
          }
          for (var i = 0; i < _this.options.prices.length; i++) {
            _this.options.prices[i].innerText = _this.options.withShipping;
          }
          for (var i = 0; i < _this.options.shippingFees.length; i++) {
            _this.options.shippingFees[i].innerText =
              _this.options.shippingCost + " TL";
          }
          document.getElementById("shipping_cost").value = _this.options.shippingCost;
        }
      });
    }
  },

  createMonth: function () {
    var currentMonth = this.date.getMonth();
    while (this.date.getMonth() === currentMonth) {
      this.createDay(
        this.date.getDate(),
        this.date.getDay(),
        this.date.getFullYear()
      );
      this.date.setDate(this.date.getDate() + 1);
    }
    // while loop trips over and day is at 30/31, bring it back
    this.date.setDate(1);
    this.date.setMonth(this.date.getMonth() - 1);

    this.label.innerHTML =
      this.monthsAsString(this.date.getMonth()) + " " + this.date.getFullYear();
    this.dateClicked();
  },

  monthsAsString: function (monthIndex) {
    return [
      "Ocak",
      "Şubat",
      "Mart",
      "Nisan",
      "Mayıs",
      "Haziran",
      "Temmuz",
      "Ağustos",
      "Eylül",
      "Ekim",
      "Kasım",
      "Aralık",
    ][monthIndex];
  },

  clearCalendar: function () {
    vanillaCalendar.month.innerHTML = "";
  },

  removeActiveClass: function () {
    for (var i = 0; i < this.activeDates.length; i++) {
      this.activeDates[i].classList.remove("vcal-date--selected");
    }
  },
};
