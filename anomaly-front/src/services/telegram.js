export function useTelegram () {
  if (window.Telegram) {
    const tg = window.Telegram.WebApp
    return { tg, user: tg.initDataUnsafe?.user }
  } else {
    return { tg: null, user: null }
  }

}
