import os
import google.generativeai as genai

api_key = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

prompt = """
اقترح فكرة فيديو يوتيوب قصير (شورت) في مجال المعلومات العامة والحقائق المثيرة.
اكتب:
1. عنوان جذاب للفيديو
2. سكريبت كامل مدته 45-60 ثانية بالعربية
3. اقتراح 3 كلمات مفتاحية للبحث عن صور/فيديوهات مناسبة له
"""

response = model.generate_content(prompt)
print("===== نتيجة الذكاء الاصطناعي =====")
print(response.text)
