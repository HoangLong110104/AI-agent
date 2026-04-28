import streamlit as st

from loader.file_loader import extract_text
from core.embedding import APIEmbedding
from core.ingest import ingest_text
from core.chroma_utils import get_chroma, get_or_create_collection
from config import EMBEDDING_ENABLED

from agent.RAG_agent import rag_agent


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(layout="wide")
st.title("Multi‑source RAG Agent")


# =====================================================
# SESSION STATE
# =====================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_summary" not in st.session_state:
    st.session_state.conversation_summary = ""

if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""


# =====================================================
# TABS 
# =====================================================
tab_ingest, tab_admin, tab_explore, tab_chat = st.tabs(
    ["📥 Ingest", "🗂️ Collections", "📚 Explore", "💬 Chat"]
)


# =====================================================
# 📥 INGEST TAB
# =====================================================
with tab_ingest:
    st.subheader("Ingest dữ liệu")

    if not EMBEDDING_ENABLED:
        st.info("Embedding đang tắt tạm thời. Bật EMBEDDING_ENABLED=true trong .env để ingest lại.")

    collection_name = st.text_input("Collection name", "default")
    files = st.file_uploader(
        "Upload files",
        type=["txt", "docx", "pptx", "pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    if st.button("Ingest", disabled=not EMBEDDING_ENABLED):
        if not files:
            st.warning("Chưa chọn file")
        else:
            client = get_chroma()
            collection = get_or_create_collection(client, collection_name)
            embedder = APIEmbedding()

            for f in files:
                text = extract_text(f)
                ingest_text(text, collection, embedder)

            st.success("✅ Ingest xong!")

# =====================================================
# 🗂️ COLLECTION ADMIN TAB
# =====================================================
with tab_admin:
    st.subheader("Quản lý collections")

    client = get_chroma()
    cols = client.list_collections()

    if not cols:
        st.info("Chưa có collection nào")
    else:
        for c in cols:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"📦 {c.name}")
            with col2:
                if st.button("Delete", key=f"del_{c.name}"):
                    client.delete_collection(c.name)
                    st.success(f"Đã xoá {c.name}")
                    st.rerun()


# =====================================================
# 📚 EXPLORE TAB
# =====================================================
with tab_explore:
    st.subheader("Xem dữ liệu trong vector DB")

    client = get_chroma()
    cols = client.list_collections()

    if not cols:
        st.info("Chưa có collection")
        st.stop()

    col_name = st.selectbox(
        "Chọn collection",
        [c.name for c in cols]
    )

    collection = get_or_create_collection(client, col_name)
    data = collection.get(
        include=["documents", "metadatas", "embeddings"]
    )

    st.write(f"Tổng vector: {len(data['ids'])}")

    for i in range(len(data["ids"])):
        with st.container(border=True):
            if data["metadatas"]:
                st.write("📄 Meta:", data["metadatas"][i])
            st.write(data["documents"][i])
            st.code(data["embeddings"][i][:10])


# =====================================================
# 💬 CHAT TAB (AGENT MỨC B – GIỮ UI CŨ)
# =====================================================
with tab_chat:
    st.subheader("Chat với Agent")

    chat_container = st.container()

    # HIỂN THỊ LỊCH SỬ CHAT
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    prompt = st.chat_input("Nhập câu hỏi...")

    if prompt:
        # --- USER ---
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)

        # --- AGENT STATE (LEVEL B) ---
        state = {
            "question": prompt,
            "history": st.session_state.messages[-6:],  # history gần nhất
            "conversation_summary": st.session_state.conversation_summary,
            "current_topic": st.session_state.current_topic,
            "context": "",
            "answer": ""
        }

        # --- RUN AGENT ---
        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    result = rag_agent.invoke(state)
                    answer = result.get("answer", "")
                    st.write(answer)

        # --- SAVE ASSISTANT ---
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        # --- UPDATE MEMORY ---
        st.session_state.conversation_summary = result.get(
            "conversation_summary",
            st.session_state.conversation_summary
        )
        st.session_state.current_topic = result.get(
            "current_topic",
            st.session_state.current_topic
        )

    st.divider()

    # DEBUG NHẸ (KHÔNG ẢNH HƯỞNG UI)
    with st.expander("🧠 Agent memory (debug)"):
        st.markdown("**Current topic:**")
        st.code(st.session_state.current_topic or "—")

        st.markdown("**Conversation summary:**")
        st.write(st.session_state.conversation_summary or "—")

    if st.button("🔄 New chat"):
        st.session_state.messages = []
        st.session_state.conversation_summary = ""
        st.session_state.current_topic = ""
        st.rerun()