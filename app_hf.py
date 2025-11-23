import gradio as gr
import json
from scorer import calculate_overall_score

def analyze_transcript(transcript_text):
    if not transcript_text or len(transcript_text.strip()) < 10:
        return "Please enter a valid transcript (at least 10 characters)."
    
    try:
        result = calculate_overall_score(transcript_text, duration_seconds=60)
        
        output = f"""
# Overall Score: {result['overall_score']:.1f} / {result['max_score']}

**Words:** {result['transcript_length']}

## Content & Structure: {result['breakdown']['content_structure']['score']:.1f}/40

## Speech Rate: {result['breakdown']['speech_rate']['score']}/10

## Language & Grammar: {result['breakdown']['language_grammar']['score']:.1f}/20

## Clarity: {result['breakdown']['clarity']['score']}/15

## Engagement: {result['breakdown']['engagement']['score']}/15

{json.dumps(result, indent=2)}



text

"""
        return output
    except Exception as e:
        return f"Error: {str(e)}"


SAMPLE = "Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. I am 13 years old. I live with my family. There are 3 people in my family, me, my mother and my father. One special thing about my family is that they are very kind hearted to everyone and soft spoken. One thing I really enjoy is play, playing cricket and taking wickets. A fun fact about me is that I see in mirror and talk by myself. One thing people don't know about me is that I once stole a toy from one of my cousin. My favorite subject is science because it is very interesting. Through science I can explore the whole world and make the discoveries and improve the lives of others. Thank you for listening."


demo = gr.Interface(
    fn=analyze_transcript,
    inputs=gr.Textbox(lines=10, placeholder="Paste transcript here...", label="Transcript", value=SAMPLE),
    outputs=gr.Markdown(label="Results"),
    title="AI Communication Scorer",
    theme="soft"
)


if __name__ == "__main__":
    demo.launch()

