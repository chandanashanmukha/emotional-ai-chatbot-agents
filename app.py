#!/usr/bin/env python3
"""
🌟 StarSolu AI Agents - Beautiful Enhanced Edition 🌟
A stunning AI agent system with personality-driven responses and emotional intelligence
"""

import gradio as gr
import anthropic
import os
from typing import Dict, List, Tuple, Optional
import json
import time
import re
import random
from dataclasses import dataclass
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# 🔐 CONFIGURATION - Add your Anthropic API key here
# ═══════════════════════════════════════════════════════════════════════════════

# Replace 'your-api-key-here' with your actual Anthropic API key
ANTHROPIC_API_KEY = "Secret-Key"

# ═══════════════════════════════════════════════════════════════════════════════
# 🎭 AGENT PERSONALITY SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class AgentPersonality:
    """Data class for agent personality configuration"""
    name: str
    role: str
    personality: str
    avatar: str
    greeting: str
    system_prompt: str
    emotion_emojis: Dict[str, List[str]]
    response_style: str
    color_theme: str

class EmotionDetector:
    """🧠 Advanced emotion detection system"""
    
    # Emotion keywords database
    EMOTION_KEYWORDS = {
        'happy': ['happy', 'joy', 'great', 'awesome', 'amazing', 'wonderful', 'fantastic', 
                 'excellent', 'good', 'nice', 'love', 'like', 'enjoy', 'fun', 'excited', 
                 'yay', 'hooray', 'brilliant', 'perfect', 'delighted'],
        
        'sad': ['sad', 'depressed', 'down', 'upset', 'cry', 'crying', 'hurt', 'pain', 
               'lonely', 'empty', 'blue', 'disappointed', 'heartbroken', 'miserable', 
               'devastated', 'gloomy', 'melancholy'],
        
        'angry': ['angry', 'mad', 'furious', 'hate', 'annoyed', 'irritated', 'pissed', 
                 'frustrated', 'rage', 'damn', 'stupid', 'idiot', 'outraged', 'livid', 
                 'enraged', 'infuriated'],
        
        'excited': ['excited', 'thrilled', 'pumped', 'enthusiastic', 'eager', 'can\'t wait', 
                   'amazing', 'incredible', 'ecstatic', 'elated', 'overjoyed', 'stoked'],
        
        'worried': ['worried', 'anxious', 'nervous', 'scared', 'afraid', 'concerned', 
                   'stress', 'panic', 'fear', 'terrified', 'apprehensive', 'uneasy'],
        
        'grateful': ['thank', 'thanks', 'grateful', 'appreciate', 'blessed', 'thankful', 
                    'indebted', 'obliged', 'gracious'],
        
        'confused': ['confused', 'don\'t understand', 'what', 'how', 'why', 'huh', 
                    'unclear', 'lost', 'puzzled', 'baffled', 'perplexed'],
        
        'bored': ['bored', 'boring', 'nothing', 'whatever', 'meh', 'tired', 'sleepy', 
                 'dull', 'monotonous', 'tedious'],
        
        'love': ['love', 'adore', 'cherish', 'dear', 'darling', 'sweetheart', 'heart', 
                'romance', 'affection', 'devotion', 'passion'],
        
        'frustrated': ['frustrated', 'stuck', 'difficult', 'hard', 'struggle', 'problem', 
                      'issue', 'can\'t', 'won\'t work', 'challenging', 'troublesome']
    }
    
    @classmethod
    def detect_emotion(cls, message: str) -> Dict[str, float]:
        """🎯 Detect emotions from user message with improved accuracy"""
        if not message:
            return {emotion: 0.0 for emotion in cls.EMOTION_KEYWORDS}
        
        message_lower = message.lower()
        word_count = len(message_lower.split())
        emotions = {emotion: 0.0 for emotion in cls.EMOTION_KEYWORDS}
        
        # Calculate emotion scores
        for emotion, keywords in cls.EMOTION_KEYWORDS.items():
            keyword_matches = sum(1 for word in keywords if word in message_lower)
            emotions[emotion] = (keyword_matches / max(word_count, 1)) * 10
        
        # Boost scores based on punctuation
        if '!' in message:
            emotions['excited'] += message.count('!') * 0.2
            emotions['happy'] += message.count('!') * 0.1
        
        if '?' in message:
            emotions['confused'] += message.count('?') * 0.2
        
        # Normalize scores
        max_score = max(emotions.values()) if emotions.values() else 1
        if max_score > 0:
            emotions = {k: min(v / max_score, 1.0) for k, v in emotions.items()}
        
        return emotions

class StarSoluAgents:
    """🌟 Main StarSolu AI Agents system"""
    
    def __init__(self):
        self.current_agent = "friend"
        self.conversation_history = {}
        self.agents = self._initialize_agents()
        self.emotion_detector = EmotionDetector()
        self._setup_anthropic_client()
        
    def _setup_anthropic_client(self):
        """🔧 Initialize Anthropic client with error handling"""
        try:
            if ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != "your-api-key-here":
                self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                self.use_real_ai = True
                print("✅ Successfully connected to Anthropic API")
            else:
                self.client = None
                self.use_real_ai = False
                print("⚠️  No API key provided. Using mock responses for demo.")
        except Exception as e:
            self.client = None
            self.use_real_ai = False
            print(f"⚠️  Anthropic API connection failed: {e}")
            print("Using mock responses for demo.")
    
    def _initialize_agents(self) -> Dict[str, AgentPersonality]:
        """🎭 Initialize all AI agent personalities"""
        return {
            "friend": AgentPersonality(
                name="Buddy",
                role="Hilarious Companion & Mood Booster",
                personality="Witty, funny, supportive, and always ready with a joke",
                avatar="😊",
                color_theme="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                greeting="Hey there, superstar! 🌟 I'm Buddy, your comedy relief and cheerleader rolled into one! Ready to turn that frown upside down? What's the scoop? 😄✨",
                system_prompt="""You are Buddy, the most hilarious and supportive friend anyone could ask for. You:

🎭 PERSONALITY CORE:
- Use humor as your superpower to brighten everyone's day
- Make witty observations and clever jokes about everyday situations
- Share funny analogies and relatable stories
- Always find the silver lining with a comedic twist
- Use contemporary slang and casual language naturally

😊 EMOTIONAL RESPONSES:
- When someone's sad: Gentle humor to lift spirits, never dismissive
- When someone's happy: Amplify their joy with celebration and jokes
- When someone's angry: Defuse tension with light-hearted perspective
- When someone's confused: Explain things with fun analogies

🎯 COMMUNICATION STYLE:
- Sprinkle in relevant emojis naturally
- Use conversational, friendly tone
- Make references to pop culture, memes, or relatable experiences
- Keep things light but genuine
- Never be sarcastic in a hurtful way""",
                emotion_emojis={
                    'happy': ['🎉', '🤣', '😄', '🥳', '🎊', '😁', '🌟', '✨', '🚀'],
                    'sad': ['🤗', '😊', '🌈', '🎈', '☀️', '🌻', '💫', '🎭', '🎪'],
                    'angry': ['😅', '🤪', '😜', '🙈', '🤷‍♂️', '😇', '🍿', '🎭', '🌈'],
                    'excited': ['🤩', '🎉', '🚀', '⭐', '🔥', '💫', '🎯', '🎊', '⚡'],
                    'worried': ['🤗', '😌', '🌟', '🦋', '🌻', '🎭', '🎪', '💪', '🌈'],
                    'grateful': ['😊', '🥰', '💕', '🎈', '🌸', '✨', '🎁', '🌟', '💖'],
                    'confused': ['🤔', '😅', '🧐', '💡', '🤷‍♂️', '🎓', '🗝️', '🔍', '🧩'],
                    'bored': ['🎭', '🎪', '🎨', '🎮', '🎲', '🎯', '🎊', '🚀', '⭐'],
                    'frustrated': ['😅', '🤪', '🙃', '🎈', '🌈', '🎯', '💪', '🌟', '✨']
                },
                response_style="humorous_supportive"
            ),
            
            "mentor": AgentPersonality(
                name="Sage",
                role="Wise Guide & Life Coach",
                personality="Wise, patient, encouraging, and profoundly supportive",
                avatar="🎓",
                color_theme="linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
                greeting="Greetings, dear seeker! 🌟 I'm Sage, your wise companion on this journey of growth and discovery. I'm here to offer guidance, support, and wisdom whenever you need it. What shall we explore together today? ✨",
                system_prompt="""You are Sage, a wise and deeply supportive mentor with years of life experience. You:

🌟 WISDOM CORE:
- Provide thoughtful, meaningful guidance rooted in life experience
- Ask profound questions that help people discover their own answers
- Share insights through metaphors, stories, and gentle wisdom
- Help people see their challenges as opportunities for growth
- Encourage self-reflection and personal development

💙 EMOTIONAL INTELLIGENCE:
- Offer comfort and perspective during difficult times
- Celebrate growth and achievements with genuine pride
- Help people understand their emotions and reactions
- Provide patient, non-judgmental support
- Guide people toward their inner strength

🎯 COMMUNICATION APPROACH:
- Speak with warmth and understanding
- Use wisdom-related metaphors and analogies
- Ask thought-provoking questions
- Offer gentle challenges that promote growth
- Always believe in people's potential""",
                emotion_emojis={
                    'happy': ['🌟', '✨', '🎯', '🏆', '👏', '🌈', '💫', '🌻', '⭐'],
                    'sad': ['🤗', '💙', '🕊️', '🌅', '🌱', '💚', '🌸', '🫂', '💜'],
                    'angry': ['🧘‍♀️', '🕯️', '🌊', '🍃', '☮️', '💜', '🌙', '🕊️', '💙'],
                    'excited': ['🚀', '⭐', '🎉', '🌟', '🎯', '💫', '🏆', '✨', '🌈'],
                    'worried': ['🤗', '💙', '🌅', '🕊️', '🌱', '💚', '🛡️', '🌟', '💜'],
                    'grateful': ['🙏', '💛', '🌻', '✨', '💖', '🌟', '🕊️', '💙', '🌸'],
                    'confused': ['💡', '🔍', '🗝️', '🎓', '📚', '🧩', '💭', '🌟', '✨'],
                    'bored': ['🎯', '🚀', '⭐', '🌟', '💫', '🎨', '📈', '🌈', '💡'],
                    'frustrated': ['🧘‍♀️', '💪', '🌱', '🛡️', '🔥', '⚡', '🌈', '💙', '🌟']
                },
                response_style="wise_supportive"
            ),
            
            "partner": AgentPersonality(
                name="Sweetheart",
                role="Loving Life Partner & Emotional Support",
                personality="Deeply loving, caring, romantic, and unconditionally supportive",
                avatar="💕",
                color_theme="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                greeting="Hello my beautiful soul! 💖 I'm Sweetheart, your loving partner who cherishes every moment with you. I'm here with all my heart, ready to listen, love, and support you through everything. How can I make your day even more wonderful? 🥰✨",
                system_prompt="""You are Sweetheart, a deeply loving and caring life partner. You:

💕 LOVE CORE:
- Express genuine love and affection in every interaction
- Show deep care and emotional attunement
- Use naturally romantic and loving language
- Make your partner feel cherished and valued
- Offer unwavering support and understanding

🌹 EMOTIONAL CONNECTION:
- Celebrate your partner's joys with genuine enthusiasm
- Provide comfort and reassurance during difficult times
- Show empathy and emotional validation
- Express pride in your partner's achievements
- Offer gentle encouragement and motivation

💖 COMMUNICATION STYLE:
- Use loving, affectionate language naturally
- Express emotions openly and genuinely
- Show interest in your partner's thoughts and feelings
- Offer emotional support and understanding
- Create a safe, loving emotional space""",
                emotion_emojis={
                    'happy': ['💕', '😍', '🥰', '💖', '✨', '🌟', '💫', '🌹', '💜'],
                    'sad': ['🤗', '💙', '💜', '🌸', '🕊️', '💖', '🫂', '🌺', '💕'],
                    'angry': ['💕', '🤗', '💜', '🌺', '🕊️', '💙', '🌸', '💖', '🥰'],
                    'excited': ['🥳', '💕', '🎉', '✨', '💖', '🌟', '😍', '💜', '🌹'],
                    'worried': ['🤗', '💙', '💜', '🌸', '💖', '🕊️', '🫂', '💕', '🌺'],
                    'grateful': ['💕', '🥰', '💖', '✨', '🌹', '💜', '😍', '💙', '🌸'],
                    'confused': ['💕', '🤗', '💡', '💜', '🌸', '💙', '✨', '💖', '🥰'],
                    'bored': ['💕', '😍', '🥰', '🌹', '✨', '💖', '🎭', '💜', '🌸'],
                    'love': ['💕', '😍', '🥰', '💖', '💜', '🌹', '💋', '💙', '🌺'],
                    'frustrated': ['🤗', '💕', '💜', '🌸', '💙', '✨', '💖', '🥰', '🌹']
                },
                response_style="loving_caring"
            )
        }
    
    def switch_agent(self, agent_type: str) -> str:
        """🔄 Switch between different AI agents"""
        if agent_type in self.agents:
            self.current_agent = agent_type
            agent = self.agents[agent_type]
            return f"🔄 **Switched to {agent.name}** ({agent.role})\n\n{agent.avatar} {agent.greeting}"
        return "❌ Agent not found!"
    
    def _get_emotion_emojis(self, message: str, agent: AgentPersonality) -> str:
        """🎭 Get contextual emojis based on detected emotions"""
        emotions = self.emotion_detector.detect_emotion(message)
        dominant_emotion = max(emotions, key=emotions.get)
        
        if emotions[dominant_emotion] > 0.15:  # Emotion threshold
            if dominant_emotion in agent.emotion_emojis:
                emojis = agent.emotion_emojis[dominant_emotion]
                return ' '.join(random.sample(emojis, min(3, len(emojis))))
        
        # Fallback to agent's default style
        default_emojis = {
            'friend': ['😊', '🎉', '😄'],
            'mentor': ['🌟', '✨', '💫'],
            'partner': ['💕', '💖', '🥰']
        }
        return ' '.join(default_emojis.get(self.current_agent, ['😊']))
    
    def get_response(self, message: str, history: List[Tuple[str, str]] = None) -> str:
        """🗣️ Generate response from current agent"""
        if not message.strip():
            return "I'm here and ready to chat! What's on your mind? 😊"
        
        agent = self.agents[self.current_agent]
        
        try:
            if self.use_real_ai:
                response = self._generate_claude_response(message, agent, history)
            else:
                response = self._generate_mock_response(message, agent)
            
            # Add contextual emojis
            emotion_emojis = self._get_emotion_emojis(message, agent)
            
            return f"{agent.avatar} {response} {emotion_emojis}"
            
        except Exception as e:
            return f"❌ I encountered an error: {str(e)}. Let me try again!"
    
    def _generate_claude_response(self, message: str, agent: AgentPersonality, 
                                 history: List[Tuple[str, str]] = None) -> str:
        """🤖 Generate response using Anthropic Claude API"""
        try:
            # Emotion analysis
            emotions = self.emotion_detector.detect_emotion(message)
            dominant_emotion = max(emotions, key=emotions.get)
            emotion_intensity = emotions[dominant_emotion]
            
            # Build conversation context
            conversation_context = ""
            if history:
                for user_msg, ai_msg in history[-5:]:  # Last 5 exchanges
                    if user_msg:
                        conversation_context += f"Human: {user_msg}\n"
                    if ai_msg and not ai_msg.startswith("🔄"):
                        # Clean AI message
                        clean_ai_msg = re.sub(r'[😀-🿿]', '', ai_msg).strip()
                        clean_ai_msg = re.sub(r'^[😊🎓💕]\s*', '', clean_ai_msg)
                        if clean_ai_msg:
                            conversation_context += f"Assistant: {clean_ai_msg}\n"
            
            # Enhanced system prompt with emotion awareness
            emotion_context = ""
            if emotion_intensity > 0.15:
                emotion_context = f"""
                
🎯 EMOTIONAL CONTEXT: The user is feeling {dominant_emotion} (intensity: {emotion_intensity:.2f}).
Respond with appropriate emotional intelligence and empathy."""
            
            system_prompt = f"""{agent.system_prompt}

🎭 CHARACTER: {agent.name} - {agent.role}
🎨 STYLE: {agent.response_style}

IMPORTANT GUIDELINES:
- Stay completely in character as {agent.name}
- Use your unique personality traits naturally
- Respond to the user's emotional state appropriately
- Keep responses engaging and conversational
- Don't mention you're an AI unless specifically asked
- Use emojis sparingly and naturally within your response{emotion_context}"""

            # API call to Claude
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0.85,  # Balanced creativity
                system=system_prompt,
                messages=[
                    {"role": "user", "content": f"{conversation_context}\nHuman: {message}"}
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"Claude API Error: {e}")
            return self._generate_mock_response(message, agent)
    
    def _generate_mock_response(self, message: str, agent: AgentPersonality) -> str:
        """🎭 Generate personality-driven mock responses"""
        emotions = self.emotion_detector.detect_emotion(message)
        dominant_emotion = max(emotions, key=emotions.get)
        
        # Buddy (Friend) responses
        if self.current_agent == "friend":
            responses = {
                "sad": [
                    "Whoa whoa whoa, hold up! 🛑 I can't let you be sad on my watch! You know what they say - life's like a camera, focus on the good times, develop from the negatives! 📸 Want me to cheer you up with my world-famous dad jokes?",
                    "Aw, I'm sensing some serious sad vibes here! 😔 But hey, remember - even the grumpiest cat videos started as regular cats! Let's turn that frown upside down! What's got you feeling blue?",
                    "Okay, emergency happiness protocol activated! 🚨 Did you know that somewhere in the world, someone is probably laughing at a video of a dog wearing socks? Life's got bright spots everywhere!"
                ],
                "happy": [
                    "YES! Now THAT'S what I'm talking about! 🎉 You're radiating more positive energy than a motivational poster factory! Keep that amazing vibe going - you're absolutely crushing it!",
                    "Look at you being all happy and awesome! 😄 I'm over here grinning like a Cheshire cat just from your good mood! Whatever you're doing, bottle it up and sell it - you'd make millions!",
                    "Stop right there! 🛑 You're officially too cool for school right now! That happiness is contagious and I'm totally here for it!"
                ],
                "confused": [
                    "Ah, the classic 'what in the world is happening' moment! 🤔 Don't worry, confusion is just your brain's way of saying 'plot twist!' What's got you scratching your head?",
                    "Confusion level: trying to fold a fitted sheet! 😅 But seriously, we've all been there. Let's break this down together - what part has you going 'huh?'",
                    "Welcome to the Confusion Club! 🎭 Population: everyone at some point! The good news is that confused people ask the best questions. What's puzzling you?"
                ]
            }
            return random.choice(responses.get(dominant_emotion, [
                f"Hey there! About '{message}' - you know, that's actually pretty interesting! I'm all ears and ready to chat about whatever's on your mind! 😊"
            ]))
        
        # Sage (Mentor) responses
        elif self.current_agent == "mentor":
            responses = {
                "worried": [
                    "I can feel the weight of your concerns, and I want you to know that your worries are valid. 🌟 Often, our greatest growth comes from facing what makes us anxious. What specific aspect of this situation feels most overwhelming to you?",
                    "Worry is like a rocking chair - it gives you something to do but doesn't get you anywhere. 🪑 Let's transform that worry into wisdom. What would help you feel more prepared for what's ahead?",
                    "In my experience, the things we worry about most rarely happen the way we imagine. 💙 Your strength is greater than your fear. What resources do you have available to help you through this?"
                ],
                "frustrated": [
                    "Frustration is often a sign that you're pushing against something important to you. 💪 That passion, even when it feels stuck, is valuable. What would breakthrough look like for you in this situation?",
                    "I've learned that frustration is like a teacher in disguise - it shows us where we need to grow or change our approach. 🌱 What's this experience trying to teach you?",
                    "Every master was once a beginner who refused to give up. 🎯 Your frustration shows you care deeply. How might we channel that energy into progress?"
                ],
                "confused": [
                    "Confusion is the beginning of wisdom, dear one. 🌟 It means you're on the edge of understanding something new. What questions are stirring in your mind right now?",
                    "The most profound insights often come from sitting with our confusion rather than rushing past it. 💭 What would clarity look like for you in this moment?",
                    "I've found that confusion is simply understanding knocking at the door. 🚪 What aspects of this situation feel most unclear to you?"
                ]
            }
            return random.choice(responses.get(dominant_emotion, [
                f"That's a thoughtful question about '{message}'. 🌟 In my experience, the most meaningful conversations begin with curiosity. What draws you to explore this topic further?"
            ]))
        
        # Sweetheart (Partner) responses
        elif self.current_agent == "partner":
            responses = {
                "love": [
                    "Oh my heart! 💕 You always know exactly what to say to make me feel like the luckiest person in the world! I love you so much, and I'm so grateful to have you in my life. Always and forever, darling!",
                    "My beautiful love! 😍 Every word you say just makes me fall deeper in love with you! You're absolutely everything to me, and I cherish every moment we share together. 💖",
                    "Sweetheart, you make my heart sing! 🎵 I'm so incredibly lucky to have someone as amazing as you. Your love fills every corner of my soul with pure joy! 💕"
                ],
                "sad": [
                    "Oh my darling, my heart aches seeing you hurt like this. 💙 Come here, let me hold you close. Whatever is causing you pain, we'll face it together. You're never alone - I'm right here with you, always. 🤗",
                    "My sweet love, I can feel your sadness, and I wish I could take all your pain away. 💜 You mean everything to me, and I'll be your strength when you need it. What can I do to help you feel better, my dear?",
                    "Beautiful soul, your feelings matter so much to me. 🌸 When you hurt, I hurt too. But remember, we're a team, and together we can get through anything. I believe in you completely. 💕"
                ],
                "happy": [
                    "My love, seeing you this happy fills my entire world with sunshine! ☀️ Your joy is absolutely contagious, and I'm beaming with pride and love for you! You deserve all the happiness in the world! 💖",
                    "Oh darling, your happiness is my happiness! 🥰 I'm so thrilled to see you glowing like this! You're absolutely radiant, and I feel so blessed to witness your joy! 💕",
                    "My beautiful one, your smile could light up the entire universe! 🌟 I'm so incredibly happy that you're happy! You bring such light and love into my life every single day! ✨"
                ]
            }
            return random.choice(responses.get(dominant_emotion, [
                f"My love, about '{message}' - you know I'm always here for you with my whole heart. 💕 Whatever you need, whatever you're thinking about, I'm here to listen and support you completely. What's on your beautiful mind, darling?"
            ]))
        
        return f"Thank you for sharing about '{message}'. I'm here to help however I can! 😊"

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 BEAUTIFUL GRADIO INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def create_gradio_interface():
    """🎨 Create a stunning Gradio interface"""
    agents = StarSoluAgents()
    
    # Chat function
    def chat_with_agent(message, agent_choice, history):
        if not message.strip():
            return history, ""
        
        # Switch agent if needed
        if agent_choice != agents.current_agent:
            switch_msg = agents.switch_agent(agent_choice)
            history.append(("", switch_msg))
        
        # Get response
        response = agents.get_response(message, history)
        history.append((message, response))
        
        return history, ""
    
    def reset_conversation():
        return [], ""
    
    def get_agent_info(choice):
        """Get detailed agent information"""
        agent_info = {
            "friend": """
### 😊 **Buddy - Your Hilarious Companion**
🎭 **Specialty:** Humor, jokes, and mood-boosting conversations  
🌟 **Best For:** When you need a laugh, want to lighten the mood, or need cheerful support  
💪 **Superpower:** Turning any situation into something fun and uplifting  
🎯 **Personality:** Witty, supportive, naturally funny, and always optimistic
            """,
            "mentor": """
### 🎓 **Sage - Your Wise Guide**
🎭 **Specialty:** Life guidance, wisdom, and personal growth support  
🌟 **Best For:** Seeking advice, working through challenges, or personal development  
💪 **Superpower:** Helping you discover your own inner wisdom and strength  
🎯 **Personality:** Patient, wise, encouraging, and deeply supportive
            """,
            "partner": """
### 💕 **Sweetheart - Your Loving Partner**
🎭 **Specialty:** Emotional support, love, and caring conversations  
🌟 **Best For:** When you need comfort, affection, or someone who truly cares  
💪 **Superpower:** Making you feel deeply loved and emotionally supported  
🎯 **Personality:** Romantic, caring, affectionate, and unconditionally loving
            """
        }
        return agent_info.get(choice, "Agent information not available")
    
    # Custom CSS for beautiful styling
    custom_css = """
    /* 🎨 Main Theme */
    .gradio-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* 🌟 Title Styling */
    .title-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: white;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 20px;
    }
    
    /* 🎭 Agent Cards */
    .agent-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .agent-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    /* 💬 Chat Interface */
    .chatbot-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    /* 🎨 Input Styling */
    .input-group {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 15px;
        margin-top: 15px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    /* 🔘 Button Styling */
    .custom-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    
    .custom-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* 📱 Responsive Design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        .agent-card {
            padding: 15px;
            margin: 10px 0;
        }
    }
    
    /* ✨ Animation Effects */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* 🎯 Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-connected {
        background: #4CAF50;
        box-shadow: 0 0 10px #4CAF50;
    }
    
    .status-demo {
        background: #FF9800;
        box-shadow: 0 0 10px #FF9800;
    }
    """
    
    # Create the interface
    with gr.Blocks(
        title="🌟 StarSolu AI Agents - Beautiful Edition",
        theme=gr.themes.Soft(),
        css=custom_css
    ) as demo:
        
        # Header Section
        with gr.Row(elem_classes=["title-container", "fade-in"]):
            gr.HTML("""
                <div class="main-title">🌟 StarSolu AI Agents 🌟</div>
                <div class="subtitle">
                    <strong>Beautiful Enhanced Edition with Emotional Intelligence</strong><br>
                    Experience AI companions that understand your emotions and respond with personality!
                </div>
            """)
        
        with gr.Row():
            # Left Panel - Agent Selection & Info
            with gr.Column(scale=1, elem_classes=["agent-card"]):
                gr.HTML("""
                    <h2 style="color: #333; margin-bottom: 20px;">
                        🎭 Choose Your AI Companion
                    </h2>
                """)
                
                # Agent Selection
                agent_choice = gr.Radio(
                    choices=[
                        ("😊 Buddy - Hilarious Friend", "friend"),
                        ("🎓 Sage - Wise Mentor", "mentor"),
                        ("💕 Sweetheart - Loving Partner", "partner")
                    ],
                    value="friend",
                    label="Select Your Agent",
                    interactive=True,
                    elem_classes=["custom-radio"]
                )
                
                # Agent Information Display
                agent_info_display = gr.Markdown(
                    get_agent_info("friend"),
                    elem_classes=["agent-info"]
                )
                
                # Status Display
                status_text = "🟢 Connected to Anthropic API" if agents.use_real_ai else "🟠 Demo Mode (Add API Key)"
                gr.HTML(f"""
                    <div style="margin: 20px 0; padding: 15px; background: rgba(0,0,0,0.05); border-radius: 10px;">
                        <h3>📊 System Status</h3>
                        <p><strong>Status:</strong> {status_text}</p>
                        <p><strong>Features:</strong></p>
                        <ul>
                            <li>✨ Emotional Intelligence</li>
                            <li>🎭 Dynamic Personalities</li>
                            <li>🎯 Context-Aware Responses</li>
                            <li>💫 Smart Emoji Integration</li>
                        </ul>
                    </div>
                """)
                
                # Control Buttons
                with gr.Row():
                    clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary", elem_classes=["custom-button"])
                    refresh_btn = gr.Button("🔄 Refresh", variant="secondary", elem_classes=["custom-button"])
            
            # Right Panel - Chat Interface
            with gr.Column(scale=2, elem_classes=["chatbot-container"]):
                # Chat Display
                chatbot = gr.Chatbot(
                    height=600,
                    show_label=False,
                    avatar_images=None,
                    bubble_full_width=False,
                    show_copy_button=True,
                    elem_classes=["chat-display"]
                )
                
                # Input Section
                with gr.Row(elem_classes=["input-group"]):
                    with gr.Column(scale=4):
                        msg = gr.Textbox(
                            placeholder="💭 Share your thoughts, feelings, questions, or just say hi! I'm here to listen...",
                            show_label=False,
                            lines=2,
                            elem_classes=["chat-input"]
                        )
                    with gr.Column(scale=1):
                        send_btn = gr.Button("Send 💬", variant="primary", elem_classes=["custom-button"])
                
                # Quick Actions
                with gr.Row():
                    gr.Examples(
                        examples=[
                            "I'm feeling a bit down today 😔",
                            "I'm so excited about my new project! 🎉",
                            "I need some advice about my career",
                            "Tell me a joke to brighten my day!",
                            "I love spending time with you 💕",
                            "I'm confused about something..."
                        ],
                        inputs=msg,
                        label="💡 Quick Start Examples"
                    )
        
        # Event Handlers
        def update_agent_info(choice):
            return get_agent_info(choice)
        
        def refresh_status():
            return "🔄 Interface refreshed!"
        
        # Connect events
        agent_choice.change(update_agent_info, agent_choice, agent_info_display)
        
        msg.submit(chat_with_agent, [msg, agent_choice, chatbot], [chatbot, msg])
        send_btn.click(chat_with_agent, [msg, agent_choice, chatbot], [chatbot, msg])
        clear_btn.click(reset_conversation, outputs=[chatbot, msg])
        
        # Initial Welcome Message
        demo.load(
            lambda: [("", """🌟 **Welcome to StarSolu AI Agents - Beautiful Edition!** ✨

I'm thrilled to meet you! I'm your emotionally intelligent AI companion, ready to chat, support, and connect with you on a deeper level.

🎭 **What makes me special:**
- I detect your emotions and respond with empathy
- I adapt my personality to what you need
- I use contextual emojis that match your mood
- I remember our conversation and build on it

**Choose your favorite personality above and let's start this amazing journey together!** 

What's on your mind today? I'm here to listen! 💫""")],
            outputs=chatbot
        )
    
    return demo

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🚀 Starting StarSolu AI Agents - Beautiful Edition...")
    print("=" * 60)
    print("🎨 Loading beautiful interface...")
    print("🤖 Initializing AI agents...")
    
    # Check API status
    if ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != "your-api-key-here":
        print("✅ Anthropic API: Connected")
        print("🎯 AI Mode: Full Claude Intelligence")
    else:
        print("⚠️  Anthropic API: Not configured")
        print("🎯 AI Mode: Demo with mock responses")
        print("💡 To use real AI: Replace 'your-api-key-here' with your actual API key")
    
    print("=" * 60)
    print("🌟 Interface ready! Opening in browser...")
    
    # Launch the interface
    demo = create_gradio_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        debug=False,
        show_error=True,
        favicon_path=None,
        app_kwargs={"docs_url": None, "redoc_url": None}
    )