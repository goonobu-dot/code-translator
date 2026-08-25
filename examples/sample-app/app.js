// お知らせ配信と注文整理を行う小さな業務アプリ(デモ用)
const mailApi = require("./lib/mail");
const db = require("./lib/db");
const log = require("./lib/log");

// 利用者にリマインドメールを送る
async function sendReminder(user) {
  if (!user.email) {
    return; // メールアドレスが無ければ何もしない
  }
  const message = "こんにちは " + user.name + " さん。未処理の注文があります。";
  await mailApi.send(user.email, message);
  log.info("sent reminder", user.email);
}

// 古い注文をまとめて削除する
function deleteOldOrders(days) {
  const limit = daysAgo(days);
  db.orders.deleteWhere("created < '" + limit + "'");
}

function daysAgo(days) {
  const d = new Date();
  d.setDate(d.getDate() - days);
  return d.toISOString();
}

module.exports = { sendReminder, deleteOldOrders };
