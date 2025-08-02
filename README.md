# 📊 Input Data Format

## 🔧 Main Structure
```json
{
    "etp": "dict",
    "eip": "dict",
    "idp": "dict",
    "vqac": "dict",
    "index": "int"
}
```

## Workflow:
- Nhận dataframe từ dữ liệu đầu vào có định dạng dữ liệu như trên.
- Clean data, xác định Label.
- Tổng hợp lại số lượng, tỉ lệ các cột category/numeric.
- Lập báo cáo thống kê.

## 📝 ETP (Evaluate Text Prompt)

```jsonc
{
  "txt_grammar": {
    "Score_for_question": 0,  // integer from 0–10
    "Reason_for_question": "string",
    "Score_for_answers": [0, 0, 0],  // list[int]
    "Reason_for_answers": ["string1", "string2", "string3"]  // list[str]
  },
  "txt_unambiguity": {
    "Score_for_question": 0,  // integer from 0–10
    "Reason_for_question": "string",
    "Score_for_answers": [0, 0, 0],  // list[int]
    "Reason_for_answers": ["string1", "string2", "string3"]  // list[str]
  },
  "txt_qa_structure": {
    "Score_for_question": 0,  // integer from 0–10
    "Reason_for_question": "string",
    "Score_for_answers": [0, 0, 0],  // list[int]
    "Reason_for_answers": ["string1", "string2", "string3"]  // list[str]
  },
  "syntactic_complexity": {
    "Score_for_question": 0,  // integer from 0–10
    "Reason_for_question": "string",
    "Score_for_answers": [0, 0, 0],  // list[int]
    "Reason_for_answers": ["string1", "string2", "string3"]  // list[str]
  },
  "language_naturalness": {
    "Score_for_question": 0,  // integer from 0–10
    "Reason_for_question": "string",
    "Score_for_answers": [0, 0, 0],  // list[int]
    "Reason_for_answers": ["string1", "string2", "string3"]  // list[str]
  }
}
```

## 🖼️ EIP (Evaluate Image Prompt)

```jsonc
{
  "img_clarity": {
    "Score": 0,        // integer between 0 and 10
    "Reason": "string"
  },
  "img_occlusion": {
    "Score": 0,        // integer between 0 and 10
    "Reason": "string"
  },
  "img_diff_ability": {
    "Score": 0,        // integer between 0 and 10
    "Reason": "string"
  },
  "img_object_density": {
    "Score": 0         // integer between 0 and 10
  },
  "img_interaction_level": {
    "Score": 0,        // integer between 0 and 10
    "Reason": "string"
  },
  "img_scene_clutter": {
    "Score": 0         // integer between 0 and 10
  }
}
```

## 📝 IDP (Image Diversity Prompt)

```jsonc
{
  "Img_scene_type": "string",              // e.g., "kitchen", "street", etc.
  "Img_main_object": "string",             // primary object in the image
  "Image_mainobj_descrip": "string",       // description of the main object
  "Cultural_context": "string",            // e.g., "Western", "Asian", etc.
  "Demographic_signals": "string",         // age, gender, clothing cues, etc.
  "Scene_typicality_score": 1              // integer from 1 to 5
}
```

## 📝 VQAC (Visual Question Answers Correlation Prompt)

```jsonc

{
  "question_to_image": {
    "response": "Yes",         // or "No"
    "reason": "string"
  },
  "answer_to_image": {
    "response": ["Yes", "No"],       // one for each answer
    "overall_response": "Yes",       // or "No" — "Yes" if ≥50% are Yes
    "reason": ["string1", "string2"] // one reason per answer
  },
  "question_to_answer": {
    "response": ["Yes", "No"],       // one for each answer
    "overall_response": "No",        // or "Yes"
    "reason": ["string1", "string2"] // one reason per answer
  },
  "guess_the_answer": {
    "response": "No",          // or "Yes"
    "reason": "string"
  },
  "reason_depth": {
    "response": 3,             // integer from 1 to 5 (reasoning level)
    "reason": "string"
  }
}
