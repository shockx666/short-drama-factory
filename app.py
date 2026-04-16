import streamlit as st
import google.generativeai as genai

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="AI 每日小说工坊",
    page_icon="✍️",
    layout="wide"
)

# --- 2. 侧边栏：设置与模型控制 ---
with st.sidebar:
    st.title("⚙️ 控制面板")
    api_key = st.text_input("第一步：输入 Gemini API Key", type="password", help="请从 Google AI Studio 获取")
    
    st.divider()
    
    st.subheader("🎨 创作设定")
    writing_style = st.selectbox(
        "选择文风", 
        ["硬核科幻", "悬疑惊悚", "职业写实", "奇幻冒险", "现代都市", "古典武侠"]
    )
    
    temperature = st.slider(
        "创意随机度", 
        min_value=0.0, max_value=1.0, value=0.7, 
        help="数值越高，脑洞越大；数值越低，逻辑越写实。"
    )
    
    st.info("数值越高，脑洞越大；数值越低，逻辑越写实")

# --- 3. 主界面布局 ---
st.title("✍️ AI 每日小说工坊")
st.caption("基于 Google Gemini 3 驱动的深度创作工具")

# 输入区分两列
col1, col2 = st.columns([2, 1])

with col1:
    user_requirement = st.text_area(
        "今日创作指令", 
        placeholder="在这里输入具体的情节点。例如：\n描述护林员身处寂静森林中的孤独感，以及他意外发现飞船残骸时的心理冲击...", 
        height=250
    )

with col2:
    story_type = st.text_input("具体子类型", "废土科幻 / 生存")
    target_words = st.select_slider(
        "目标字数",
        options=[500, 1000, 2000, 3000, 4000, 5000],
        value=2000
    )

# --- 4. 生成逻辑 ---
if st.button("开始创作 ✨", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ 请先在左侧输入 API Key。")
    elif not user_requirement:
        st.warning("⚠️ 请输入今天的创作灵感。")
    else:
        try:
            # 初始化模型
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-3-flash-preview')
            
            with st.status("🚀 AI 正在构思剧情...", expanded=True) as status:
                st.write("正在连接大语言模型...")
                
                # 针对职业写作者优化的 Prompt
                prompt = f"""
                你是一位文学造诣极高的职业小说家，擅长构建深刻的世界观。
                请根据以下要求进行创作：
                
                【核心任务】
                - 故事类型：{story_type}
                - 文学风格：{writing_style}
                - 目标字数：约 {target_words} 字
                - 创作指令：{user_requirement}
                
                【写作准则】
                1. 拒绝平铺直叙：通过角色的感官（听觉、嗅觉、触觉）来侧面烘托环境。
                2. 深度心理分析：重点刻画角色在极端环境或未知事物面前的心理张力。
                3. 专业性细节：如果涉及野外生存、森林管理或科技操作，请融入准确的专业术语或细节描写。
                4. 避免说教：让故事自己说话，结尾要留有余味。
                
                请直接输出正文，保持排版优雅。
                """
                
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(temperature=temperature)
                )
                status.update(label="✅ 创作完成！", state="complete", expanded=False)

            # 结果展示
            st.success("故事生成成功：")
            st.markdown(f"---")
            st.markdown(response.text)
            
            # 导出功能
            st.download_button(
                label="📥 下载草稿 (TXT)",
                data=response.text,
                file_name=f"{story_type}_draft.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"生成过程中出现错误：{str(e)}")

# --- 5. 底部 ---
st.divider()
st.caption("保持每日书写，灵感永不枯竭。建议将生成的文本作为草稿进行二次润色。")