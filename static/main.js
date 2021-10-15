function cc(name) {
  document.querySelector('.spinner1').style.display = 'flex';
  
  $.get('/price_checker?q=' + name, function (results) {
    document.querySelector('.spinner1').style.display = 'none';
    var nameSplit = name.split('$');
    var type = nameSplit[1];
    var monthly = results;
    var security = monthly * 2;
    var actual_price = parseInt(monthly) + parseInt(security);
    var coupon = actual_price / 10 * 4;
    var total = actual_price - coupon;
    document.querySelector("#monthly").innerHTML = 'Monthly fee (1st Month): $' + monthly;
    document.querySelector("#security").innerHTML = 'Security deposit: $' + security;
    document.querySelector("#total").innerHTML = 'Total: $' + actual_price;
    document.querySelector("#coupon").innerHTML = 'You save: $' + coupon;
    document.querySelector("#strike").innerHTML = '$' + actual_price;
    document.querySelector("#order_total").innerHTML = '$' + total;
    document.querySelector("#changeType").innerHTML = 'Type: ' + type;
    document.querySelector("#type_changer2").innerHTML = 'Type: ' + type;
    document.querySelector("#selectType1").value = type;
    document.querySelector("#selectType2").value = type;
    document.querySelector("#h_type_value").value = type;
    document.querySelector("#price").value = total;
    document.querySelector("#h_type_valuePy").value = type;
    document.querySelector("#h_type_valueSv").value = type;
    document.querySelector("#pricePy").value = total;
    document.querySelector("#priceSv").value = total;
  })
}