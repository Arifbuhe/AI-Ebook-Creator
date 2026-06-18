import streamlit as st
import google.generativeai as genai
import time

# 1. Konfigurasi Tampilan Halaman
st.set_page_config(page_title="Pro Ebook Generator", page_icon="🚀", layout="wide")

# 2. Mengambil API Key dari Brankas Rahasia (Tanpa input pengguna)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except KeyError:
    st.error("Sistem sedang perbaikan: API Key tidak ditemukan di server.")
    st.stop()

# 3. Simulasi Sistem Saldo Koin
if "koin" not in st.session_state:
    st.session_state.koin = 1  

# 4. SIDEBAR: Dompet & Top-Up
with st.sidebar:
    st.header("⚙️ Dashboard Pengguna")
    st.markdown("---")
    st.subheader("💰 Dompet Anda")
    st.metric(label="Koin Tersedia", value=f"{st.session_state.koin} 🪙")
    st.info("Biaya: 1 Koin / Ebook")
    
    st.markdown("Habis koin? Beli paket di bawah ini:")
    if st.button("💳 Top-Up 5 Koin (Rp 50.000)", use_container_width=True):
        st.session_state.koin += 5
        st.success("Pembayaran berhasil! Koin bertambah.")
        time.sleep(1)
        st.rerun()

# 5. AREA UTAMA: Tampilan Aplikasi & Kategori Profesional
st.title("🚀 Premium AI Ebook Creator")
st.markdown("Isi detail di bawah ini untuk meracik ebook profesional berkualitas tinggi. **(Biaya: 1 Koin)**")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Detail Utama")
    topic = st.text_input("💡 Topik Ebook", placeholder="Contoh: Trik Rahasia Review Barang Cepat Viral")
    tujuan = st.selectbox("🎯 Tujuan Ebook", [
        "Lead Magnet (Untuk pancingan klik link affiliate/promosi)", 
        "Buku Edukasi/Panduan Teknis", 
        "Cerita Fiksi/Naratif Hiburan",
        "Modul Pelatihan Pribadi"
    ])
    target = st.selectbox("👥 Target Pembaca", ["Pemula", "Menengah", "Profesional/Ahli", "Umum"])

with col2:
    st.markdown("### 🎨 Personalisasi Ekstra")
    sudut_pandang = st.selectbox("👁️ Sudut Pandang Penulis", [
        "Orang Pertama (Gunakan kata 'Saya' atau 'Aku')", 
        "Orang Pertama Jamak (Gunakan kata 'Kami')", 
        "Pihak Ketiga Ekspert (Objektif)"
    ])
    gaya_bahasa = st.selectbox("🎭 Gaya Bahasa", [
        "Santai & Menghibur (Seperti curhat dengan teman)", 
        "Formal & Profesional", 
        "Storytelling (Bercerita yang dramatis & mengalir)"
    ])
    panjang_tulisan = st.select_slider("📏 Estimasi Kepadatan Materi", options=["Ringkas (To-the-point)", "Standar", "Sangat Detail & Mendalam"])

st.markdown("##")

# 6. TOMBOL EKSEKUSI
if st.button("✨ Generate Ebook (Bayar 1 🪙)", type="primary", use_container_width=True):
    if not topic:
        st.warning("⚠️ Topik ebook tidak boleh kosong!")
    elif st.session_state.koin <= 0:
        st.error("❌ Koin Anda tidak cukup! Silakan Top-Up di menu sebelah kiri.")
    else:
        with st.spinner("🔮 AI sedang meracik ebook premium Anda..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Merakit instruksi (Prompt) Super Spesifik
                prompt = f"""
                Bertindaklah sebagai penulis buku best-seller dan ahli materi. Buatkan draf ebook lengkap dan terstruktur berdasarkan instruksi ini:
                - Topik: {topic}
                - Tujuan Buku: {tujuan} (Sesuaikan isi buku agar mencapai tujuan ini)
                - Target Pembaca: {target}
                - Sudut Pandang: {sudut_pandang}
                - Gaya Bahasa: {gaya_bahasa}
                - Tingkat Kedalaman: {panjang_tulisan}
                
                Struktur yang wajib ada:
                1. Judul Buku yang memikat (Sertakan sub-judul).
                2. Kata Pengantar yang membangun kedekatan.
                3. Pendahuluan.
                4. Minimal 3 Bab Inti (Berikan langkah-langkah praktis dan aplikatif).
                5. Kesimpulan & Call to Action (Dorong pembaca melakukan tindakan sesuai tujuan buku).
                
                Penting: Jika gaya bahasa 'Santai & Menghibur', selipkan selingan candaan, analogi ringan, atau cerita pendek agar pembaca tidak merasa sedang membaca buku teks yang kaku. Gunakan format teks Markdown yang rapi.
                """
                
                response = model.generate_content(prompt)
                ebook_result = response.text
                
                st.session_state.koin -= 1
                st.success(f"🎉 Ebook berhasil dibuat! Sisa koin Anda: {st.session_state.koin} 🪙")
                
                st.markdown("---")
                st.markdown(ebook_result)
                st.markdown("---")
                
                st.download_button(
                    label="📥 Download Hasil Ebook",
                    data=ebook_result,
                    file_name=f"Ebook_{topic[:15].replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")
