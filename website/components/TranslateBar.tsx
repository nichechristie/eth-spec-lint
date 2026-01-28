"use client";

export default function TranslateBar() {
  function handleChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const lang = e.target.value;
    if (lang) {
      const url = `https://translate.google.com/translate?sl=en&tl=${lang}&u=${encodeURIComponent(window.location.href)}`;
      window.location.href = url;
    }
  }

  return (
    <div className="flex items-center justify-center gap-3 border-b border-white/5 bg-white/[0.02] px-4 py-2 text-sm">
      <label htmlFor="language-select" className="text-slate-400">
        Translate this page:
      </label>
      <select
        id="language-select"
        onChange={handleChange}
        className="rounded-lg border border-white/10 bg-white/5 px-3 py-1.5 text-sm text-slate-300 outline-none transition-colors hover:border-purple-500/30 focus:border-purple-500/50"
      >
        <option value="">Select Language</option>
        <option value="af">Afrikaans</option>
        <option value="sq">Albanian (Shqip)</option>
        <option value="am">Amharic (አማርኛ)</option>
        <option value="ar">Arabic (العربية)</option>
        <option value="hy">Armenian (Հայերեն)</option>
        <option value="as">Assamese (অসমীয়া)</option>
        <option value="ay">Aymara</option>
        <option value="az">Azerbaijani (Azərbaycan)</option>
        <option value="bm">Bambara</option>
        <option value="eu">Basque (Euskara)</option>
        <option value="be">Belarusian (Беларуская)</option>
        <option value="bn">Bengali (বাংলা)</option>
        <option value="bho">Bhojpuri (भोजपुरी)</option>
        <option value="bs">Bosnian (Bosanski)</option>
        <option value="bg">Bulgarian (Български)</option>
        <option value="ca">Catalan (Català)</option>
        <option value="ceb">Cebuano</option>
        <option value="ny">Chichewa</option>
        <option value="zh-CN">Chinese Simplified (简体中文)</option>
        <option value="zh-TW">Chinese Traditional (繁體中文)</option>
        <option value="co">Corsican (Corsu)</option>
        <option value="hr">Croatian (Hrvatski)</option>
        <option value="cs">Czech (Čeština)</option>
        <option value="da">Danish (Dansk)</option>
        <option value="dv">Dhivehi (ދިވެހި)</option>
        <option value="doi">Dogri (डोगरी)</option>
        <option value="nl">Dutch (Nederlands)</option>
        <option value="en">English</option>
        <option value="eo">Esperanto</option>
        <option value="et">Estonian (Eesti)</option>
        <option value="ee">Ewe (Eʋegbe)</option>
        <option value="fil">Filipino (Tagalog)</option>
        <option value="fi">Finnish (Suomi)</option>
        <option value="fr">French (Français)</option>
        <option value="fy">Frisian (Frysk)</option>
        <option value="gl">Galician (Galego)</option>
        <option value="ka">Georgian (ქართული)</option>
        <option value="de">German (Deutsch)</option>
        <option value="el">Greek (Ελληνικά)</option>
        <option value="gn">Guarani (Avañe&#39;ẽ)</option>
        <option value="gu">Gujarati (ગુજરાતી)</option>
        <option value="ht">Haitian Creole (Kreyòl)</option>
        <option value="ha">Hausa</option>
        <option value="haw">Hawaiian (ʻŌlelo Hawaiʻi)</option>
        <option value="he">Hebrew (עברית)</option>
        <option value="hi">Hindi (हिन्दी)</option>
        <option value="hmn">Hmong</option>
        <option value="hu">Hungarian (Magyar)</option>
        <option value="is">Icelandic (Íslenska)</option>
        <option value="ig">Igbo (Asụsụ Igbo)</option>
        <option value="ilo">Ilocano</option>
        <option value="id">Indonesian (Bahasa Indonesia)</option>
        <option value="ga">Irish (Gaeilge)</option>
        <option value="it">Italian (Italiano)</option>
        <option value="ja">Japanese (日本語)</option>
        <option value="jv">Javanese (Basa Jawa)</option>
        <option value="kn">Kannada (ಕನ್ನಡ)</option>
        <option value="kk">Kazakh (Қазақ)</option>
        <option value="km">Khmer (ភាសាខ្មែរ)</option>
        <option value="rw">Kinyarwanda</option>
        <option value="gom">Konkani (कोंकणी)</option>
        <option value="ko">Korean (한국어)</option>
        <option value="kri">Krio</option>
        <option value="ku">Kurdish (Kurmanji)</option>
        <option value="ckb">Kurdish (Sorani)</option>
        <option value="ky">Kyrgyz (Кыргызча)</option>
        <option value="lo">Lao (ພາສາລາວ)</option>
        <option value="la">Latin (Latina)</option>
        <option value="lv">Latvian (Latviešu)</option>
        <option value="ln">Lingala (Lingála)</option>
        <option value="lt">Lithuanian (Lietuvių)</option>
        <option value="lg">Luganda (Oluganda)</option>
        <option value="lb">Luxembourgish (Lëtzebuergesch)</option>
        <option value="mk">Macedonian (Македонски)</option>
        <option value="mai">Maithili (मैथिली)</option>
        <option value="mg">Malagasy</option>
        <option value="ms">Malay (Bahasa Melayu)</option>
        <option value="ml">Malayalam (മലയാളം)</option>
        <option value="mt">Maltese (Malti)</option>
        <option value="mi">Maori (Te Reo Māori)</option>
        <option value="mr">Marathi (मराठी)</option>
        <option value="mni-Mtei">Meiteilon (Manipuri)</option>
        <option value="lus">Mizo (Mizo ṭawng)</option>
        <option value="mn">Mongolian (Монгол)</option>
        <option value="my">Myanmar (မြန်မာ)</option>
        <option value="ne">Nepali (नेपाली)</option>
        <option value="no">Norwegian (Norsk)</option>
        <option value="or">Odia (ଓଡ଼ିଆ)</option>
        <option value="om">Oromo (Afaan Oromoo)</option>
        <option value="ps">Pashto (پښتو)</option>
        <option value="fa">Persian (فارسی)</option>
        <option value="pl">Polish (Polski)</option>
        <option value="pt">Portuguese (Português)</option>
        <option value="pa">Punjabi (ਪੰਜਾਬੀ)</option>
        <option value="qu">Quechua (Runasimi)</option>
        <option value="ro">Romanian (Română)</option>
        <option value="ru">Russian (Русский)</option>
        <option value="sm">Samoan (Gagana Samoa)</option>
        <option value="sa">Sanskrit (संस्कृतम्)</option>
        <option value="gd">Scots Gaelic (Gàidhlig)</option>
        <option value="nso">Sepedi</option>
        <option value="sr">Serbian (Српски)</option>
        <option value="st">Sesotho</option>
        <option value="sn">Shona (chiShona)</option>
        <option value="sd">Sindhi (سنڌي)</option>
        <option value="si">Sinhala (සිංහල)</option>
        <option value="sk">Slovak (Slovenčina)</option>
        <option value="sl">Slovenian (Slovenščina)</option>
        <option value="so">Somali (Soomaali)</option>
        <option value="es">Spanish (Español)</option>
        <option value="su">Sundanese (Basa Sunda)</option>
        <option value="sw">Swahili (Kiswahili)</option>
        <option value="sv">Swedish (Svenska)</option>
        <option value="tg">Tajik (Тоҷикӣ)</option>
        <option value="ta">Tamil (தமிழ்)</option>
        <option value="tt">Tatar (Татар)</option>
        <option value="te">Telugu (తెలుగు)</option>
        <option value="th">Thai (ไทย)</option>
        <option value="ti">Tigrinya (ትግርኛ)</option>
        <option value="ts">Tsonga (Xitsonga)</option>
        <option value="tr">Turkish (Türkçe)</option>
        <option value="tk">Turkmen (Türkmen)</option>
        <option value="ak">Twi (Akan)</option>
        <option value="uk">Ukrainian (Українська)</option>
        <option value="ur">Urdu (اردو)</option>
        <option value="ug">Uyghur (ئۇيغۇرچە)</option>
        <option value="uz">Uzbek (O&#39;zbek)</option>
        <option value="vi">Vietnamese (Tiếng Việt)</option>
        <option value="cy">Welsh (Cymraeg)</option>
        <option value="xh">Xhosa (isiXhosa)</option>
        <option value="yi">Yiddish (ייִדיש)</option>
        <option value="yo">Yoruba (Yorùbá)</option>
        <option value="zu">Zulu (isiZulu)</option>
      </select>
      <span className="text-xs text-slate-600">133 Languages</span>
    </div>
  );
}
