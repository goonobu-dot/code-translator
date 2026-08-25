// 設定(デモ用)
module.exports = {
  mailHost: "https://mail.example-service.com",
  stripeKey: process.env.STRIPE_KEY, // 秘密鍵はコードに書かず、環境変数から読み込む
  logLevel: "info",
};
