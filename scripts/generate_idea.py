import os
import json
import google.generativeai as genai

api_key = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-3.6-flash")

BASE_PROMPT = """
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

SCORE_PROMPT = """
إنت خبير محتوى يوتيوب متخصص في الشورتس الفيرال. قيّم السكريبت ده بصرامة شديدة من 0 لـ100
بناءً على المعايير دي بالظبط:
1. قوة أول جملة (Hook) - هل تخلي حد يوقف السكرول فعلاً في أول ثانيتين؟
2. الإيقاع والتشويق - هل كل جملة بتخلي الشخص عايز يعرف الجملة الجاية؟
3. القيمة الحقيقية للمعلومة - هل مفيدة أو مثيرة فعلاً ولا سطحية؟
4. قوة الدعوة للفعل في النهاية

السكريبت:
{script}

رد بصيغة JSON فقط بالشكل ده:
{{
  "score": رقم من 0 إلى 100,
  "feedback": "سبب مختصر ومحدد للنقص لو فيه، أو سبب القوة لو ممتاز"
}}
"""

def generate_idea(feedback=None):
    prompt = BASE_PROMPT
    if feedback:
        prompt += f"\n\nملاحظة: المحاولة اللي فاتت كانت ضعيفة للسبب ده: \"{feedback}\"\nاكتب فكرة جديدة تمامًا تتجنب المشكلة دي."

    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    return json.loads(response.text)

def score_idea(data):
    script_text = f"العنوان: {data['title']}\n\n"
    for s in data["scenes"]:
        script_text += f"- {s['voice_text']}\n"
    script_text += f"\nCTA: {data['cta_text']}"

    response = model.generate_content(
        SCORE_PROMPT.format(script=script_text),
        generation_config={"response_mime_type": "application/json"}
    )
    return json.loads(response.text)

def main():
    max_attempts = 3
    feedback = None
    best_result = None

    for attempt in range(1, max_attempts + 1):
        print(f"\n===== المحاولة {attempt} =====")
        idea = generate_idea(feedback)
        evaluation = score_idea(idea)
        score = evaluation["score"]
        feedback = evaluation["feedback"]

        print(f"العنوان: {idea['title']}")
        print(f"النتيجة: {score}%")
        print(f"الملاحظات: {feedback}")

        if best_result is None or score > best_result["quality_score"]:
            idea["quality_score"] = score
            idea["quality_feedback"] = feedback
            best_result = idea

        if score >= 80:
            print(f"\n✅ الفكرة اتقبلت من المحاولة {attempt} بنتيجة {score}%")
            break
    else:
        print(f"\n⚠️ ما وصلناش لـ 80% بعد {max_attempts} محاولات - هنستخدم أفضل نتيجة ({best_result['quality_score']}%)")

    os.makedirs("output", exist_ok=True)
    with open("output/idea.json", "w", encoding="utf-8") as f:
        json.dump(best_result, f, ensure_ascii=False, indent=2)

    print("\n===== الفكرة النهائية =====")
    print(json.dumps(best_result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
