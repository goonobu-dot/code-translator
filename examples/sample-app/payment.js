// 注文確定と課金の処理(デモ用)
const stripeApi = require("./lib/stripe");
const db = require("./lib/db");

// 注文を確定してカードへ課金する
async function confirmOrder(order) {
  const total = order.items.reduce((sum, item) => sum + item.price, 0);
  const charge = await stripeApi.charge(order.cardToken, total, "JPY");
  db.orders.save({ ...order, chargeId: charge.id, status: "paid" });
  return charge.id;
}

module.exports = { confirmOrder };
