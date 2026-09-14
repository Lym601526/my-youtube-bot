import os
import json
import google.generativeai as genai

api_key = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-3.6-flash")

prompt = """
اقترح فكرة فيديو يوتيوب قصير (شورت) في مجال المعلومات العامة والحقائق المثيرة.

مهم جدًا: رد بصيغة JSON فقط بدون أي نص زيادة قبله أو بعده، بالشكل ده بالظبط:

{
  "title": "عنوان جذاب للفيديو",
  "scenes": [
    {"voice_text": "الجملة اللي هتتقال بالصوت", "visual_keyword": "English search keyword for footage"}
  ],
  "cta_text": "جملة دعوة للمتابعة في الآخر"
}

اكتب من 5 إلى 7 مشاهد (scenes)، كل مشهد جملة صوت واحدة قصيرة بالعربية،
وكلمة بحث بالإنجليزي مناسبة لمقطع فيديو حر الحقوق يمثل الجملة دي.
"""

response = model.generate_content(
    prompt,
    generation_config={"response_mime_type": "application/json"}
)

data = json.loads(response.text)

os.makedirs("output", exist_ok=True)
with open("output/idea.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("===== تم إنشاء الفكرة =====")
print(json.dumps(data, ensure_ascii=False, indent=2))
