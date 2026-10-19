import os, zipfile, shutil, textwrap

project = "/mnt/data/pintar-matematika-sd-streamlit"
os.makedirs(os.path.join(project, "assets"), exist_ok=True)

app_py = r'''import streamlit as st
import math
import json
from pathlib import Path

st.set_page_config(
    page_title="Pintar Matematika SD",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family: 'Nunito', sans-serif;}
.hero {background:linear-gradient(120deg,#e2f2ff,#f0f5ff 58%,#fff2d3);padding:1.5rem 1.8rem;border-radius:24px;margin-bottom:1rem;}
.hero h1 {color:#18365c;font-size:2.2rem;margin-bottom:.3rem;}
.hero p {color:#536985;font-size:1.05rem;}
.pill {display:inline-block;background:#e8f2ff;color:#246bd6;border-radius:20px;padding:5px 12px;font-weight:800;font-size:.8rem;}
.lesson {background:#fff;border:1px solid #e7edf5;border-radius:18px;padding:1rem 1.1rem;margin-bottom:.8rem;}
.formula {background:#edf6ff;color:#18365c;border-radius:16px;padding:1rem;text-align:center;font-size:1.5rem;font-weight:900;}
div.stButton > button {border-radius:12px;font-weight:800;}
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

MATERI = [
    {"id":"numbers","title":"Bilangan & Operasi Hitung","grade":1,"category":"Aritmetika","emoji":"🔢","summary":"Kenali angka, tambah, kurang, dan strategi berhitung.","formula":"a + b = jumlah","concept":"Penjumlahan menggabungkan dua kelompok benda. Pengurangan berarti mengambil sebagian atau mencari selisih.","example":"Ada 7 apel lalu ditambah 5 apel. Berapa jumlah apel sekarang?","steps":["Tuliskan bilangan: 7 + 5.","Mulai dari 7, lanjutkan 5 hitungan: 8, 9, 10, 11, 12.","Jadi, jumlahnya adalah 12 apel."],"answer":"12 apel"},
    {"id":"division","title":"Pembagian Cepat","grade":3,"category":"Aritmetika","emoji":"➗","summary":"Pahami pembagian sebagai kebalikan perkalian.","formula":"a ÷ b = c, jika b × c = a","concept":"Pembagian membagi jumlah menjadi kelompok sama banyak. Gunakan perkalian untuk membantu menemukan hasil pembagian.","example":"Hitung 156 ÷ 12 dengan cepat.","steps":["Cari kelipatan 12: 12 × 10 = 120.","Sisa bilangan: 156 − 120 = 36.","12 × 3 = 36, jadi tambahkan 3 kelompok.","10 + 3 = 13. Maka 156 ÷ 12 = 13."],"answer":"13"},
    {"id":"flat","title":"Luas Persegi & Persegi Panjang","grade":3,"category":"Geometri","emoji":"🟦","summary":"Hitung luas dengan ukuran sisi.","formula":"Persegi: L = s × s | Persegi panjang: L = p × l","concept":"Luas adalah ukuran daerah di dalam bentuk. Keliling adalah panjang seluruh sisi yang mengelilingi bentuk.","example":"Persegi memiliki sisi 6 cm. Berapa luasnya?","steps":["Catat panjang sisi: 6 cm.","Gunakan rumus L = s × s.","L = 6 × 6 = 36."],"answer":"36 cm²"},
    {"id":"cube","title":"Volume Kubus","grade":5,"category":"Bangun Ruang","emoji":"🧊","summary":"Temukan ruang yang dapat diisi sebuah kubus.","formula":"V = s × s × s = s³","concept":"Kubus memiliki enam sisi persegi yang sama besar. Volume mengukur ruang yang ditempati bangun ruang.","example":"Sebuah kubus memiliki rusuk 4 cm. Berapa volumenya?","steps":["Panjang rusuk s = 4 cm.","Masukkan ke rumus: V = 4 × 4 × 4.","Hitung 4 × 4 = 16, lalu 16 × 4 = 64.","Tuliskan satuan kubik: 64 cm³."],"answer":"64 cm³"},
    {"id":"cuboid","title":"Volume Balok","grade":5,"category":"Bangun Ruang","emoji":"📦","summary":"Hitung volume dari panjang, lebar, dan tinggi.","formula":"V = p × l × t","concept":"Balok memiliki panjang, lebar, dan tinggi. Kalikan ketiga ukuran untuk memperoleh volume.","example":"Balok panjang 8 cm, lebar 3 cm, tinggi 2 cm. Berapa volumenya?","steps":["Catat p = 8 cm, l = 3 cm, t = 2 cm.","Gunakan rumus V = p × l × t.","V = 8 × 3 × 2 = 48."],"answer":"48 cm³"},
    {"id":"distance","title":"Jarak, Kecepatan & Waktu","grade":5,"category":"Pengukuran","emoji":"🚲","summary":"Hubungkan jarak perjalanan, kecepatan, dan waktu.","formula":"Jarak = kecepatan × waktu","concept":"Jika kecepatan tetap, jarak sama dengan kecepatan dikalikan lama perjalanan. Pastikan satuan waktu sesuai.","example":"Sepeda bergerak 12 km/jam selama 3 jam. Berapa jaraknya?","steps":["Kecepatan = 12 km/jam.","Waktu = 3 jam.","Jarak = 12 × 3 = 36 km."],"answer":"36 km"},
    {"id":"sqrt","title":"Akar Kuadrat","grade":6,"category":"Bilangan","emoji":"√","summary":"Cari bilangan yang dikalikan dirinya menghasilkan bilangan tertentu.","formula":"√a = b jika b × b = a","concept":"Akar kuadrat adalah kebalikan pangkat dua. Untuk kuadrat sempurna, hasilnya bilangan bulat.","example":"Sebuah persegi luasnya 64 cm². Berapa panjang sisinya?","steps":["Luas persegi = sisi × sisi.","Sisi = √64.","Karena 8 × 8 = 64, maka √64 = 8."],"answer":"8 cm"},
    {"id":"fraction","title":"Pecahan Senilai","grade":4,"category":"Pecahan","emoji":"🍕","summary":"Pahami bagian dari keseluruhan dan pecahan senilai.","formula":"a/b = (a × n)/(b × n), n ≠ 0","concept":"Pecahan menunjukkan bagian dari keseluruhan. Pecahan senilai memiliki nilai sama meskipun pembilang dan penyebut berbeda.","example":"Sederhanakan pecahan 6/8.","steps":["Cari bilangan yang membagi 6 dan 8, yaitu 2.","Bagi pembilang dan penyebut dengan 2.","6 ÷ 2 = 3 dan 8 ÷ 2 = 4."],"answer":"3/4"},
    {"id":"percent","title":"Persen","grade":5,"category":"Pecahan","emoji":"💯","summary":"Ubah persen menjadi bagian dari seratus.","formula":"Persentase nilai = persen ÷ 100 × nilai","concept":"Persen berarti per seratus. Misalnya, 25% sama dengan 25/100 atau seperempat.","example":"Berapakah 25% dari 200?","steps":["Ubah 25% menjadi 25/100.","Hitung 25/100 × 200.","Hasilnya adalah 50."],"answer":"50"},
    {"id":"circle","title":"Luas & Keliling Lingkaran","grade":6,"category":"Geometri","emoji":"🟠","summary":"Gunakan jari-jari atau diameter untuk menghitung lingkaran.","formula":"L = π × r² | K = 2 × π × r","concept":"Jari-jari adalah jarak dari pusat ke tepi lingkaran. Diameter adalah dua kali jari-jari. Gunakan π sekitar 3,14 atau 22/7 sesuai soal.","example":"Lingkaran berjari-jari 7 cm. Hitung kelilingnya dengan π = 22/7.","steps":["Diketahui r = 7 cm.","K = 2 × π × r.","K = 2 × 22/7 × 7 = 44."],"answer":"44 cm"},
    {"id":"average","title":"Rata-rata","grade":6,"category":"Data","emoji":"📊","summary":"Temukan rata-rata dari sekumpulan data.","formula":"Rata-rata = jumlah seluruh data ÷ banyak data","concept":"Rata-rata diperoleh dengan menjumlahkan semua nilai, lalu membaginya dengan jumlah data.","example":"Nilai 6, 8, dan 10. Berapa rata-ratanya?","steps":["Jumlahkan: 6 + 8 + 10 = 24.","Ada 3 data.","Rata-rata = 24 ÷ 3 = 8."],"answer":"8"},
    {"id":"units","title":"Konversi Satuan Panjang","grade":3,"category":"Pengukuran","emoji":"📏","summary":"Ubah satuan mm, cm, m, dan km.","formula":"1 m = 100 cm | 1 km = 1.000 m","concept":"Pahami hubungan antar satuan. Dari satuan besar ke satuan lebih kecil biasanya dikalikan; arah sebaliknya dibagi.","example":"Berapa sentimeter dalam 3 meter?","steps":["Ingat 1 m = 100 cm.","Kalikan 3 × 100.","Jadi, 3 m = 300 cm."],"answer":"300 cm"},
]

SOAL = [
    {"grade":3,"q":"Berapakah 72 ÷ 8?","options":["7","8","9","10"],"correct":2,"explain":"Karena 8 × 9 = 72, maka 72 ÷ 8 = 9."},
    {"grade":5,"q":"Kubus memiliki rusuk 3 cm. Berapa volumenya?","options":["9 cm³","18 cm³","27 cm³","36 cm³"],"correct":2,"explain":"Volume kubus = 3 × 3 × 3 = 27 cm³."},
    {"grade":5,"q":"Kecepatan 10 km/jam selama 2 jam. Berapa jaraknya?","options":["5 km","12 km","20 km","30 km"],"correct":2,"explain":"Jarak = kecepatan × waktu = 10 × 2 = 20 km."},
    {"grade":6,"q":"Berapakah √81?","options":["7","8","9","10"],"correct":2,"explain":"Karena 9 × 9 = 81, maka √81 = 9."},
    {"grade":4,"q":"Pecahan 4/8 paling sederhana adalah...","options":["1/4","1/2","2/3","4/4"],"correct":1,"explain":"Pembilang dan penyebut dibagi 4: 4/8 = 1/2."},
    {"grade":5,"q":"Berapakah 20% dari 150?","options":["20","25","30","35"],"correct":2,"explain":"20/100 × 150 = 30."},
]

def init_state():
    defaults = {"page":"Beranda","grade":1,"lesson_id":None,"done":[],"quiz_index":0,"quiz_answers":{},"quiz_checked":False,"scores":[],"calc_history":[]}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
init_state()

def show_header(eyebrow, title, subtitle):
    st.markdown(f'<div class="hero"><span class="pill">{eyebrow}</span><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def home():
    show_header("PETUALANGAN ANGKA DIMULAI", "Halo, Jagoan Matematika! 🌟", "Belajar rumus, coba tantangan, dan temukan serunya matematika.")
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader("Pilih kelasmu")
        grade = st.radio("Kelas", [1,2,3,4,5,6], index=st.session_state.grade-1, horizontal=True, label_visibility="collapsed")
        st.session_state.grade = grade
        st.caption(f"Materi pilihan untuk Kelas {grade}")
        if st.button("📚 Mulai belajar", type="primary", use_container_width=True):
            st.session_state.page = "Materi"; st.rerun()
    with col2:
        st.markdown("<div class='lesson' style='text-align:center;font-size:4rem'>🦉<br><span style='font-size:1rem;font-weight:800;color:#246bd6'>Ayo belajar!</span></div>", unsafe_allow_html=True)
    st.subheader("Jelajahi matematika")
    a,b,c = st.columns(3)
    with a:
        if st.button("📖 Materi & Rumus", use_container_width=True): st.session_state.page="Materi"; st.rerun()
    with b:
        if st.button("🧮 Kalkulator", use_container_width=True): st.session_state.page="Kalkulator"; st.rerun()
    with c:
        if st.button("🎯 Kuis", use_container_width=True): st.session_state.page="Kuis"; st.rerun()
    st.info("Mode prototipe: materi contoh disertakan di aplikasi. Streamlit biasanya membutuhkan koneksi untuk menjalankan server, jadi offline penuh berbeda dari PWA.")

def materials():
    show_header("PERPUSTAKAAN RUMUS", "Materi & Rumus 📚", "Pilih materi untuk memahami konsep, rumus, contoh soal, dan penyelesaiannya.")
    c1,c2,c3 = st.columns([1,1,2])
    with c1:
        grade = st.selectbox("Kelas", ["Semua kelas",1,2,3,4,5,6], index=[ "Semua kelas",1,2,3,4,5,6].index(st.session_state.grade))
    with c2:
        cats = ["Semua kategori"] + sorted(set(x["category"] for x in MATERI))
        category = st.selectbox("Kategori", cats)
    with c3:
        search = st.text_input("Cari materi", placeholder="Misalnya: akar, volume, pembagian")
    filtered = [x for x in MATERI if (grade=="Semua kelas" or x["grade"]==grade) and (category=="Semua kategori" or x["category"]==category) and search.lower() in (x["title"]+" "+x["summary"]+" "+x["category"]).lower()]
    if not filtered:
        st.warning("Materi tidak ditemukan. Coba ubah filter pencarian.")
    cols = st.columns(2)
    for i, item in enumerate(filtered):
        with cols[i%2]:
            with st.container(border=True):
                st.markdown(f"### {item['emoji']} {item['title']}")
                st.caption(f"Kelas {item['grade']} · {item['category']}")
                st.write(item["summary"])
                if st.button("Pelajari materi →", key=f"open_{item['id']}", use_container_width=True):
                    st.session_state.lesson_id=item["id"]; st.session_state.page="Detail materi"; st.rerun()

def lesson_detail():
    item = next((x for x in MATERI if x["id"]==st.session_state.lesson_id), None)
    if not item:
        st.session_state.page="Materi"; st.rerun()
    if st.button("← Kembali ke materi"):
        st.session_state.page="Materi"; st.rerun()
    show_header(f"KELAS {item['grade']} · {item['category'].upper()}", f"{item['emoji']} {item['title']}", item["concept"])
    st.markdown(f"<div class='formula'>{item['formula']}</div>", unsafe_allow_html=True)
    st.subheader("📝 Contoh soal")
    st.markdown(f"<div class='lesson'><b>{item['example']}</b></div>", unsafe_allow_html=True)
    st.subheader("Penyelesaian langkah demi langkah")
    for step in item["steps"]:
        st.markdown(f"- {step}")
    st.success(f"Jawaban: {item['answer']}")
    if st.button("✅ Tandai sudah dipelajari", type="primary"):
        if item["id"] not in st.session_state.done:
            st.session_state.done.append(item["id"])
        st.toast("Materi ditandai sudah dipelajari!")
    st.caption("Materi contoh prototipe; sebaiknya diperiksa guru dan disesuaikan dengan kurikulum yang digunakan.")

def calculator():
    show_header("ALAT BANTU BELAJAR", "Kalkulator Pintar 🧮", "Hitung dengan teliti dan lihat langkah penjelasan sederhana.")
    with st.form("calculator_form"):
        expr = st.text_input("Masukkan operasi", placeholder="Contoh: (156 / 12) + 4")
        st.caption("Operator yang didukung: +, -, *, /, tanda kurung, pangkat dengan **, dan fungsi sqrt(...).")
        submitted = st.form_submit_button("Hitung", type="primary")
    if submitted:
        try:
            import ast
            tree = ast.parse(expr, mode="eval")
            allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd, ast.Load, ast.Call, ast.Name)
            if any(not isinstance(n, allowed_nodes) for n in ast.walk(tree)):
                raise ValueError("Operasi tidak didukung. Gunakan angka dan operator matematika.")
            if any(isinstance(n, ast.Name) and n.id != "sqrt" for n in ast.walk(tree)):
                raise ValueError("Nama fungsi yang didukung hanya sqrt.")
            if any(isinstance(n, ast.Call) and (not isinstance(n.func, ast.Name) or n.func.id != "sqrt" or len(n.args)!=1 or n.keywords) for n in ast.walk(tree)):
                raise ValueError("Format fungsi yang didukung: sqrt(angka).")
            result = eval(compile(tree, "<calc>", "eval"), {"__builtins__": {}}, {"sqrt": math.sqrt})
            if not isinstance(result, (int,float)) or not math.isfinite(result):
                raise ValueError("Hasil tidak valid.")
            result = round(result, 10)
            st.success(f"Hasil: **{result}**")
            st.write(f"Ekspresi yang dihitung: `{expr} = {result}`")
            st.session_state.calc_history.append(f"{expr} = {result}")
        except Exception as ex:
            st.error(f"Belum bisa dihitung: {ex}")
    with st.expander("Riwayat perhitungan"):
        if st.session_state.calc_history:
            for item in reversed(st.session_state.calc_history[-10:]):
                st.write("• " + item)
            if st.button("Hapus riwayat"):
                st.session_state.calc_history=[]
                st.rerun()
        else:
            st.caption("Belum ada perhitungan.")

def quiz():
    show_header("TANTANGAN HARI INI", "Kuis Matematika 🎯", "Pilih jawaban, periksa, lalu baca pembahasannya.")
    idx = st.session_state.quiz_index % len(SOAL)
    q = SOAL[idx]
    st.caption(f"Soal {idx+1} dari {len(SOAL)} · Kelas {q['grade']}")
    st.subheader(q["q"])
    choice = st.radio("Pilih jawaban", q["options"], key=f"answer_{idx}", index=None)
    if st.button("Periksa jawaban", type="primary", disabled=choice is None):
        st.session_state.quiz_answers[idx] = choice
        st.session_state.quiz_checked = True
        is_correct = choice == q["options"][q["correct"]]
        st.session_state.scores.append(is_correct)
    if st.session_state.quiz_checked:
        chosen = st.session_state.quiz_answers.get(idx)
        if chosen == q["options"][q["correct"]]:
            st.success("Hebat! Jawabanmu benar 🎉")
        else:
            st.warning(f"Belum tepat. Jawaban yang benar: {q['options'][q['correct']]}")
        st.info(q["explain"])
        if st.button("Soal berikutnya →"):
            st.session_state.quiz_index = (idx+1) % len(SOAL)
            st.session_state.quiz_checked = False
            st.rerun()

def progress():
    show_header("PERJALANAN BELAJARMU", "Progres Belajar ⭐", "Lihat materi yang telah dipelajari dan hasil latihan di sesi ini.")
    a,b,c = st.columns(3)
    with a: st.metric("Materi selesai", len(st.session_state.done))
    with b: st.metric("Soal diperiksa", len(st.session_state.scores))
    with c: st.metric("Jawaban benar", sum(st.session_state.scores))
    if st.session_state.done:
        st.subheader("Materi yang sudah dipelajari")
        for id_ in st.session_state.done:
            item = next((x for x in MATERI if x["id"]==id_), None)
            if item: st.write(f"✅ {item['title']}")
    else:
        st.info("Belum ada materi yang ditandai selesai. Buka materi dan tekan tombol tandai selesai.")
    st.caption("Pada versi ini progres disimpan selama sesi Streamlit berjalan. Untuk penyimpanan permanen, tambahkan database atau penyimpanan lokal.")

with st.sidebar:
    st.markdown("## 🦉 Pintar Matematika")
    st.caption("Belajar jadi menyenangkan!")
    page = st.radio("Navigasi", ["Beranda","Materi","Kalkulator","Kuis","Progres"], index=["Beranda","Materi","Kalkulator","Kuis","Progres"].index(st.session_state.page) if st.session_state.page in ["Beranda","Materi","Kalkulator","Kuis","Progres"] else 1)
    st.session_state.page = page
    st.divider()
    st.markdown("**Kelas target**")
    st.write("Kelas 1–6 SD")
    st.markdown("---")
    st.caption("Hak Cipta : @yulidiana67_pare")

if st.session_state.page == "Beranda": home()
elif st.session_state.page == "Materi": materials()
elif st.session_state.page == "Detail materi": lesson_detail()
elif st.session_state.page == "Kalkulator": calculator()
elif st.session_state.page == "Kuis": quiz()
elif st.session_state.page == "Progres": progress()

st.markdown("---")
st.caption("Hak Cipta : @yulidiana67_pare")
'''
with open(os.path.join(project, "app.py"), "w", encoding="utf-8") as f:
    f.write(app_py)
with open(os.path.join(project, "requirements.txt"), "w", encoding="utf-8") as f:
    f.write("streamlit>=1.40\n")
with open(os.path.join(project, "README.md"), "w", encoding="utf-8") as f:
    f.write("""# Pintar Matematika SD — Streamlit

## Menjalankan di Windows
1. Instal Python dari https://www.python.org/downloads/ dan centang **Add Python to PATH** saat instalasi.
2. Ekstrak folder proyek.
3. Buka folder di VS Code, lalu pilih Terminal → New Terminal.
4. Jalankan:
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   python -m pip install -r requirements.txt
   streamlit run app.py
   ```
5. Browser akan terbuka. Jika tidak, buka `http://localhost:8501`.

## Menjalankan di macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Fitur: beranda, materi dan rumus contoh, kalkulator, kuis, progres sesi, dan label hak cipta. Materi adalah prototipe awal yang perlu diverifikasi guru.
""")

# Include generated app icon if available in runtime.
icon_source = "/mnt/data/a_bright_colorful_high_resolution_cartoon_app_ic.png"
if os.path.exists(icon_source):
    shutil.copy2(icon_source, os.path.join(project, "assets", "icon.png"))

zip_path = "/mnt/data/pintar-matematika-sd-streamlit.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, names in os.walk(project):
        for name in names:
            full = os.path.join(root, name)
            z.write(full, os.path.relpath(full, "/mnt/data"))
print("Proyek Streamlit dibuat:", zip_path)
print("Isi proyek:", os.listdir(project))
