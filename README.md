# 🎬 Subtitle Translator

A sleek, single-file subtitle translation web app with a glassmorphism UI, dark/light theme toggle, and AI-powered SRT translation — powered by Google Gemini AI.

> Built by **Jithula Bhasitha** for [Bit X Tools](https://bit-x-tools.vercel.app)

---

## ✨ Features

- 📝 **SRT Translation** — Translate entire SRT subtitle files into natural, cinematic Sinhala
- 🤖 **AI-Powered** — Uses advanced Google Gemini models (Flash/Pro) for high-quality translation
- 🎭 **Artistic Personas** — Choose between "Funny & Witty" or "Serious Cinematic" translation styles
- 🌙 / ☀️ **Dark & Light Theme** — Toggle with a beautiful animated switch; preference saved in `localStorage`
- 📊 **Real-time Log** — Monitor the translation progress with a live batch-processing log
- ⚡ **Single File** — Entire app lives in one `index.html` — no build tools, no dependencies to install
- 📱 **Fully Responsive** — Works great on desktop, tablet, and mobile

---

## 🛠️ Built With

| Technology | Purpose |
|---|---|
| HTML5 | Structure |
| CSS3 | Glassmorphism UI, animations, responsive layout |
| Vanilla JavaScript | App logic, API calls, theme management |
| [Google Gemini API](https://aistudio.google.com/) | AI translation engine |
| [Font Awesome 6](https://fontawesome.com/) | Icons |
| [Google Fonts — Poppins](https://fonts.google.com/specimen/Poppins) | Typography |

---

## 📁 Project Structure

Since the entire app is bundled into one file, the internal structure is:

```
index.html
├── <head>
│   ├── Font Awesome CDN
│   └── Google Fonts CDN
├── <style>
│   ├── CSS variables (dark/light themes)
│   ├── Glassmorphism component styles
│   └── Responsive breakpoints
├── <body>
│   ├── Navbar (logo + back button + theme toggle)
│   ├── Hero section (title + description)
│   ├── Settings Panel
│   │   ├── API Key input
│   │   ├── File upload (SRT)
│   │   └── Model & Style configuration
│   ├── Dashboard Panel
│   │   ├── Progress bar
│   │   ├── Live translation log
│   │   └── Result preview & Export
│   └── Footer
└── <script>
    ├── SRT parsing logic
    ├── Batch processing system
    ├── Gemini API integration + fallback logic
    ├── Theme toggle + localStorage persistence
    └── Export/Download handler
```

---

## 🌐 API Reference

This project uses the [Google Generative AI (Gemini) API](https://ai.google.dev/docs/gemini_api_overview).

```
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}
```

The app processes subtitles in batches to optimize performance and handle API rate limits effectively.

---

## 🎨 UI Preview

| Dark Mode | Light Mode |
|---|---|
| Deep navy glassmorphism | Clean frosted white |
| Purple gradient accents | Purple gradient accents |
| 🌙 Moon toggle | ☀️ Sun toggle |

---

## 🐛 Known Limitations

- Requires a valid Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/)
- Translation quality depends on the selected AI model and persona
- API rate limits may apply based on your Google AI Studio tier

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">Made with ❤️ by Jithula Bhasitha for Bit X Tools</p>
