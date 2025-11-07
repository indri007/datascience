import streamlit as st
from google import genai 
import pandas as pd
import os
import io

# --- KONFIGURASI APLIKASI ---
st.set_page_config(page_title="Product Assistant Sheet", page_icon="🔗")
st.title("🔗 Asisten Produk dari Google Sheet (XLSX)")
st.caption("Jawaban diambil dari link ekspor XLSX Google Sheet menggunakan Gemini API.")

# --- 1. DEKLARASIKAN LINK EKSPOR XLSX DI SINI ---
# GANTI LINK INI dengan URL EKSPOR XLSX dari Google Sheet Anda
GOOGLE_SHEET_XLSX_URL = "https://docs.google.com/spreadsheets/d/1kyKSrPcLSSdXGV0LvHaFKGDuaI5rTWJj/export?format=xlsx&gid=2121219071"

# --- FUNGSI UNTUK MEMBACA DATA DARI LINK ---
@st.cache_data(ttl=3600)
def load_product_data(url):
    """Membaca data produk dari link XLSX Google Sheet."""
    if not url:
        return None, "URL XLSX belum diatur."
        
    try:
        # Menggunakan pd.read_excel() untuk file XLSX
        df = pd.read_excel(
            url, 
            sheet_name=0, 
            engine='openpyxl' 
        )
        
        # Membersihkan nama kolom 
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]

        # Mengubah DataFrame menjadi string format Markdown (membutuhkan 'tabulate')
        knowledge_string = df.to_markdown(index=False)
        return knowledge_string, None
    except Exception as e:
        return None, f"Gagal memuat data dari URL: {e}"

PRODUCT_KNOWLEDGE, error_message = load_product_data(GOOGLE_SHEET_XLSX_URL)

if error_message:
    st.error(f"Gagal memuat data: {error_message}")
    st.stop()

# --- 2. KONFIGURASI GEMINI ---
try:
    # Mengambil kunci API dari secrets.toml
    GOOGLE_API_KEY = st.secrets["gemini"]["GOOGLE_API_KEY"] 
    
    # Membuat objek Client untuk inisialisasi API Key
    gemini_client = genai.Client(api_key=GOOGLE_API_KEY)
    
except KeyError:
    st.error("GOOGLE_API_KEY tidak ditemukan. Pastikan sudah ada di bagian `[gemini]` dalam `.streamlit/secrets.toml`.")
    st.stop()
except Exception as e:
    st.error(f"Error konfigurasi Gemini: {e}")
    st.stop()

# --- Antarmuka Aplikasi (UI) ---

st.success("✅ Data produk berhasil dimuat dari Google Sheet.")
with st.expander("Lihat Data Produk yang Digunakan (Markdown Format)"):
    st.code(PRODUCT_KNOWLEDGE)

user_prompt = st.text_area(
    "Ajukan pertanyaan berdasarkan data sheet:", 
    placeholder="Contoh: Berapa harga 'Kursus Pemasaran Digital'?",
    height=100
)

if st.button("Tanyakan ke Gemini", type="primary"):
    if user_prompt:
        
        # --- 3. MEMBUAT PROMPT DENGAN KNOWLEDGE (RAG) ---
        final_prompt = f"""
        Anda adalah asisten penjualan yang menjawab pertanyaan.
        Jawab HANYA berdasarkan "DATA PRODUK" di bawah. Jangan tambahkan informasi lain yang tidak ada.

        --- DATA PRODUK ---
        {PRODUCT_KNOWLEDGE}
        ---

        PERTANYAAN PELANGGAN:
        {user_prompt}

        Jawaban Anda:
        """
        
        with st.spinner("Mencari jawaban dalam data sheet..."):
            try:
                # PERBAIKAN: Mengganti model='gemini-1.5-flash' menjadi model='gemini-2.5-flash'
                response = gemini_client.models.generate_content(
                    model='gemini-2.5-flash', 
                    contents=final_prompt
                )
                
                st.subheader("✅ Jawaban Gemini:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Gagal mendapatkan respons dari Gemini: {e}")
    else:
        st.warning("Mohon masukkan pertanyaan terlebih dahulu.")