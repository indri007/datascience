# 🔗 Streamlit Gemini Product Assistant

Aplikasi web interaktif (chatbot) yang dibangun menggunakan **Streamlit** dan **Gemini API** untuk menjawab pertanyaan tentang inventaris produk digital. Data produk dimuat secara langsung dari Google Sheet (format XLSX) untuk memastikan informasi selalu *up-to-date*.

## 🚀 Demo Aplikasi

Aplikasi ini di-deploy menggunakan Streamlit Community Cloud.

**Link Demo:** https://datascience-r3zq4ddvwm5w3efwabh397.streamlit.app/ 

*(Catatan: Ganti **xxxx** dengan URL demo Streamlit Community Cloud Anda setelah deployment.)*

## ✨ Fitur Utama

* **Retrieval-Augmented Generation (RAG):** Menggunakan Gemini API untuk menjawab pertanyaan berdasarkan konteks data produk.
* **Integrasi Google Sheets:** Memuat data produk secara *real-time* dari tautan ekspor XLSX Google Sheet menggunakan pustaka `pandas` dan `openpyxl`.
* **Antarmuka Streamlit:** Menyediakan *user interface* yang sederhana dan responsif.
* **Pengamanan Kunci API:** Kunci API Gemini dimuat dengan aman melalui Streamlit Secrets.

## ⚙️ Cara Menjalankan Secara Lokal

### 1. Klon Repositori

```bash
git clone [https://github.com/indri007/datascience.git](https://github.com/indri007/datascience.git)
cd datascience