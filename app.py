
import math
import streamlit as st

st.set_page_config(
    page_title="Pintar Matematika SD",
    page_icon="🦉",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}
.hero {
    padding: 28px;
    border-radius: 24px;
    background: linear-gradient(120deg, #dff2ff, #f1eaff, #fff1cc);
}
.hero h1 { color: #18365c; font-weight: 900; }
div.stButton > button {
    border-radius: 12px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

if "selesai" not in st.session_state:
    st.session_state.selesai = []
if "skor" not in st.session_state:
    st.session_state.skor = 0
if "diperiksa" not in st.session_state:
    st.session_state.diperiksa = []

MATERI = [
    {
        "judul": "Penjumlahan",
        "kelas": 1,
        "rumus": "a + b = jumlah",
        "contoh": "7 + 5 = 12",
        "penjelasan": "Penjumlahan menggabungkan dua kelompok benda."
    },
    {
        "judul": "Pembagian",
        "kelas": 3,
        "rumus": "a ÷ b = c",
        "contoh": "72 ÷ 8 = 9",
        "penjelasan": "Pembagian membagi jumlah menjadi kelompok sama banyak."
    },
    {
        "judul": "Pecahan",
        "kelas": 4,
        "rumus": "a/b",
        "contoh": "6/8 = 3/4",
        "penjelasan": "Pecahan menunjukkan bagian dari keseluruhan."
    },
    {
        "judul": "Volume Kubus",
        "kelas": 5,
        "rumus": "V = s × s × s",
        "contoh": "Jika s = 4 cm, V = 64 cm³",
        "penjelasan": "Volume mengukur ruang yang ditempati bangun."
    },
    {
        "judul": "Persentase",
        "kelas": 5,
        "rumus": "Persen / 100 × nilai",
        "contoh": "25% dari 200 = 50",
        "penjelasan": "Persen berarti per seratus."
    },
    {
        "judul": "Akar Kuadrat",
        "kelas": 6,
        "rumus": "√a = b jika b × b = a",
        "contoh": "√81 = 9",
        "penjelasan": "Akar kuadrat merupakan kebalikan dari pangkat dua."
    },
]

SOAL = [
    {
        "tanya": "Berapakah 8 × 7?",
        "opsi": ["48", "54", "56", "64"],
        "benar": "56"
    },
    {
        "tanya": "Berapakah √81?",
        "opsi": ["7", "8", "9", "10"],
        "benar": "9"
    },
    {
        "tanya": "Berapakah 25% dari 200?",
        "opsi": ["25", "40", "50", "75"],
        "benar": "50"
    },
]

st.sidebar.title("🦉 Pintar Matematika")
halaman = st.sidebar.radio(
    "Menu Utama",
    ["Beranda", "Materi & Rumus", "Kalkulator", "Kuis", "Progres"]
)
st.sidebar.caption("Hak Cipta: @yulidiana67_pare")

if halaman == "Beranda":
    st.markdown("""
    <div class="hero">
      <h1>🌟 Pintar Matematika SD</h1>
      <p>Belajar matematika dengan cara yang menyenangkan!</p>
    </div>
    """, unsafe_allow_html=True)

    kelas = st.selectbox("Pilih kelas", [1, 2, 3, 4, 5, 6])
    st.session_state.kelas = kelas

    st.subheader("Ayo mulai petualangan angka!")
    a, b, c = st.columns(3)
    a.metric("Materi tersedia", len(MATERI))
    b.metric("Materi selesai", len(st.session_state.selesai))
    c.metric("Jawaban benar", st.session_state.skor)

    st.info("Pilih menu di sebelah kiri untuk mulai belajar.")

elif halaman == "Materi & Rumus":
    st.title("📚 Materi dan Rumus")

    kelas = st.selectbox("Filter kelas", [1, 2, 3, 4, 5, 6])
    cari = st.text_input("Cari materi")

    daftar = [
        m for m in MATERI
        if m["kelas"] == kelas
        and cari.lower() in m["judul"].lower()
    ]

    if not daftar:
        st.info("Belum ada materi untuk pilihan ini.")

    for m in daftar:
        with st.expander(m["judul"]):
            st.write(m["penjelasan"])
            st.subheader("Rumus")
            st.info(m["rumus"])
            st.write("Contoh:", m["contoh"])

            if st.button("Tandai selesai", key=m["judul"]):
                if m["judul"] not in st.session_state.selesai:
                    st.session_state.selesai.append(m["judul"])
                st.success("Materi ditandai selesai.")

elif halaman == "Kalkulator":
    st.title("🧮 Kalkulator Pintar")
    st.write("Masukkan dua angka dan pilih operasi hitung.")

    a = st.number_input("Angka pertama", value=0.0)
    b = st.number_input("Angka kedua", value=1.0)
    operasi = st.selectbox(
        "Operasi",
        ["Penjumlahan", "Pengurangan", "Perkalian", "Pembagian"]
    )

    if st.button("Hitung", type="primary"):
        if operasi == "Penjumlahan":
            hasil = a + b
        elif operasi == "Pengurangan":
            hasil = a - b
        elif operasi == "Perkalian":
            hasil = a * b
        elif b == 0:
            st.error("Angka pembagi tidak boleh nol.")
            hasil = None
        else:
            hasil = a / b

        if hasil is not None:
            st.success(f"Hasil perhitungan: {hasil:g}")

elif halaman == "Kuis":
    st.title("🎯 Kuis Matematika")

    for i, soal in enumerate(SOAL):
        st.subheader(f"Soal {i + 1}")
        st.write(soal["tanya"])

        jawaban = st.radio(
            "Pilih jawaban",
            soal["opsi"],
            key=f"soal_{i}"
        )

        if st.button("Periksa", key=f"periksa_{i}"):
            if i not in st.session_state.diperiksa:
                st.session_state.diperiksa.append(i)

                if jawaban == soal["benar"]:
                    st.session_state.skor += 1

            if jawaban == soal["benar"]:
                st.success("Benar! Hebat! 🎉")
            else:
                st.warning(f"Jawaban yang benar: {soal['benar']}")

elif halaman == "Progres":
    st.title("⭐ Progres Belajar")

    st.metric("Materi selesai", len(st.session_state.selesai))
    st.metric("Jawaban benar", st.session_state.skor)
    st.metric("Soal diperiksa", len(st.session_state.diperiksa))

    for judul in st.session_state.selesai:
        st.write(f"✅ {judul}")

st.divider()
st.caption("Pintar Matematika SD · Hak Cipta: @yulidiana67_pare")
