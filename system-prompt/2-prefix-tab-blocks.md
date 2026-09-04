# Prefix Tab: Time-Awareness Block Layout

In the Agora app, switch to the **Prefix Tab** in the System Prompt editor. This configures how user messages are wrapped with real-time timestamps before being sent to the AI model. 

Here is how I set it up to give my agent a perfect sense of time:

---

### Block 1: Text Block
*Paste the following XML opening tag:*

```text
<agora_user_message sent_date="
```

---

### Block 2: Widget Block
👉 *Click the `+` button and insert the **Send Date** widget.*

---

### Block 3: Text Block
*Paste the following attribute bridge:*

```text
" sent_time="
```

---

### Block 4: Widget Block
👉 *Click the `+` button and insert the **Send Time** widget.*

---

### Block 5: Text Block
*Paste the following closing XML tag (make sure to include the blank newline at the end so it doesn't stick to your message):*

```text
">

```
