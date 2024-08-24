import streamlit as st
from openai import OpenAI

# OpenAI istemcisini oluşturun
client = OpenAI(
    api_key="YOUR_API_KEY")

# Film türleri listesi
genre_list = [
    "Aksiyon", "Macera", "Animasyon", "Komedi", "Suç", "Belgesel", "Dram", "Aile",
    "Fantezi", "Tarih", "Korku", "Müzikal", "Gizem", "Romantik", "Bilim Kurgu",
    "Gerilim", "Savaş", "Western"
]

# Sayfa konfigürasyonu
st.set_page_config(page_title="Film Öneri Asistanı", page_icon="🎬", layout="wide")

# Ana başlık
st.title("🍿 Kişiselleştirilmiş Film Önerileri")

# Nasıl Çalışır bölümü
with st.expander("📖 Nasıl Çalışır?"):
    st.write("""
    1. **Film Türleri Seçimi**: Listeden sevdiğiniz film türlerini işaretleyin. Birden fazla tür seçebilirsiniz.
    2. **Favori Filmler**: En sevdiğiniz 3 filmi girin. Bu, önerileri kişiselleştirmemize yardımcı olacak.
    3. **Önerileri Göster**: Tüm seçimlerinizi yaptıktan sonra 'Önerileri Göster' butonuna tıklayın.
    4. **Film Önerileri**: Yapay zeka, seçimlerinize göre size 5 film önerisi sunacak.
    5. **İnceleme**: Önerilen filmlerin adlarını, türlerini ve kısa özetlerini göreceksiniz.

    Not: Bu uygulama, OpenAI'nin GPT-3.5 modelini kullanarak kişiselleştirilmiş öneriler sunar. Öneriler, seçimlerinize ve AI'nın bilgi tabanına dayanır.
    """)

st.markdown("---")

# Yan panel ve ana içerik için sütunlar
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Film Tercihleriniz")

    st.write("Film Türleri:")
    selected_genres = []
    # Film türlerini 3 sütuna bölelim
    genre_columns = st.columns(3)
    for i, genre in enumerate(genre_list):
        if genre_columns[i % 3].checkbox(genre, key=f"genre_{i}"):
            selected_genres.append(genre)

    favorite_movies = []
    for i in range(3):
        movie = st.text_input(f"En sevdiğiniz {i + 1}. film:", key=f"movie_{i}")
        if movie:
            favorite_movies.append(movie)

    if st.button("🔍 Önerileri Göster", type="primary"):
        if selected_genres and len(favorite_movies) == 3:
            st.session_state.show_recommendations = True
        else:
            st.error("Lütfen en az bir film türü seçin ve üç favori film girin!")

with col2:
    st.subheader("Film Önerileri")
    if 'show_recommendations' in st.session_state and st.session_state.show_recommendations:
        prompt = f"""
        Kullanıcının sevdiği film türleri: {', '.join(selected_genres)}
        Kullanıcının en sevdiği 3 film: {', '.join(favorite_movies)}

        Lütfen bu bilgilere dayanarak, kullanıcının sevebileceği 5 film önerisi yapın. 
        Cevabınızı aşağıdaki formatta bir tablo olarak verin:

        | Film Adı | Tür | Kısa Özet |
        |----------|-----|-----------|
        | ...      | ... | ...       |

        Her film için türü ve kısa bir özet (maksimum 50 kelime) ekleyin.
        """

        with st.spinner("🎭 Film önerileri hazırlanıyor..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Sen yardımcı bir film öneri asistanısın."},
                        {"role": "user", "content": prompt}
                    ]
                )
                recommendations = response.choices[0].message.content
                st.markdown(recommendations)
            except Exception as e:
                st.error(f"Bir hata oluştu: {str(e)}")
    else:
        st.info("👈 Lütfen film tercihlerinizi girin ve 'Önerileri Göster' butonuna tıklayın.")

# Dipnot
st.markdown("---")
st.markdown("*Bu uygulama, OpenAI'nin GPT-3.5 modelini kullanarak kişiselleştirilmiş film önerileri sunar.*")