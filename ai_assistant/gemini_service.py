"""
AI Assistant service for providing hints and debugging help using Google's Gemini AI.
"""
import google.generativeai as genai
from django.conf import settings
import logging
from typing import Optional, Dict, Any

# Configure logging
logger = logging.getLogger(__name__)

class GeminiService:
    """Service class for interacting with Google's Gemini AI."""
    
    def __init__(self):
        """Initialize the Gemini service with API key."""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use Gemini 2.0 Flash Experimental - latest and most capable model
        # Available with Gemini+ subscription
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_problem_hint(self, problem_title: str, problem_description: str, 
                            difficulty: str = None) -> Optional[str]:
        """
        Generate a helpful hint for a programming problem.
        
        Args:
            problem_title: The title of the problem
            problem_description: The full problem description
            difficulty: The difficulty level of the problem
            
        Returns:
            A helpful hint as a string, or None if generation fails
        """
        try:
            prompt = f"""
            You are an experienced programming mentor helping a student with a coding problem.
            
            Problem Title: {problem_title}
            Problem Description: {problem_description}
            {f"Difficulty: {difficulty}" if difficulty else ""}
            
            Please provide a helpful hint that:
            1. Guides the student toward the solution without giving it away completely
            2. Explains the key concept or algorithm needed
            3. Suggests the general approach or data structure to use
            4. Is encouraging and educational
            
            Keep the hint concise (2-3 sentences) and focus on the most important insight.
            Do not provide the complete solution or code.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip() if response.text else None
            
        except Exception as e:
            logger.error(f"Error generating problem hint: {str(e)}")
            return None
    
    def analyze_wrong_answer(self, problem_title: str, problem_description: str,
                           user_code: str, language: str, expected_output: str = None,
                           actual_output: str = None) -> Optional[str]:
        """
        Analyze why a solution might be producing wrong answers.
        
        Args:
            problem_title: The title of the problem
            problem_description: The full problem description
            user_code: The user's submitted code
            language: Programming language used
            expected_output: Expected output (if available)
            actual_output: Actual output produced (if available)
            
        Returns:
            Analysis and suggestions as a string, or None if generation fails
        """
        try:
            prompt = f"""
            You are an experienced programming mentor helping debug a student's code.
            
            Problem Title: {problem_title}
            Problem Description: {problem_description}
            
            Student's Code ({language}):
            ```{language.lower()}
            {user_code}
            ```
            
            {f"Expected Output: {expected_output}" if expected_output else ""}
            {f"Actual Output: {actual_output}" if actual_output else ""}
            
            The code is producing "Wrong Answer". Please analyze and provide:
            1. Potential issues in the logic or implementation
            2. Common mistakes that might cause wrong answers for this type of problem
            3. Specific suggestions for what to check or fix
            4. Edge cases the student might have missed
            
            Be constructive and educational. Focus on helping them understand the mistake rather than just fixing it.
            Keep your response concise (3-4 sentences).
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip() if response.text else None
            
        except Exception as e:
            logger.error(f"Error analyzing wrong answer: {str(e)}")
            return None
    
    def analyze_runtime_error(self, problem_title: str, user_code: str, 
                            language: str, error_message: str = None) -> Optional[str]:
        """
        Analyze runtime errors and provide debugging suggestions.
        
        Args:
            problem_title: The title of the problem
            user_code: The user's submitted code
            language: Programming language used
            error_message: Runtime error message (if available)
            
        Returns:
            Analysis and suggestions as a string, or None if generation fails
        """
        try:
            prompt = f"""
            You are helping debug a runtime error in a student's code.
            
            Problem: {problem_title}
            Language: {language}
            
            Code:
            ```{language.lower()}
            {user_code}
            ```
            
            {f"Error Message: {error_message}" if error_message else "The code has a runtime error."}
            
            Please provide:
            1. What might be causing the runtime error
            2. Specific lines or patterns to check
            3. Common runtime error causes in {language}
            4. How to prevent this type of error
            
            Keep your response helpful and concise (2-3 sentences).
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip() if response.text else None
            
        except Exception as e:
            logger.error(f"Error analyzing runtime error: {str(e)}")
            return None
    
    def analyze_time_limit_exceeded(self, problem_title: str, user_code: str, 
                                  language: str) -> Optional[str]:
        """
        Analyze Time Limit Exceeded errors and suggest optimizations.
        
        Args:
            problem_title: The title of the problem
            user_code: The user's submitted code
            language: Programming language used
            
        Returns:
            Analysis and optimization suggestions as a string, or None if generation fails
        """
        try:
            prompt = f"""
            You are helping optimize a student's code that's getting "Time Limit Exceeded".
            
            Problem: {problem_title}
            Language: {language}
            
            Code:
            ```{language.lower()}
            {user_code}
            ```
            
            Please analyze and suggest:
            1. What might be causing the timeout (algorithm complexity, inefficient operations)
            2. More efficient algorithms or data structures to use
            3. Specific optimizations for this code
            4. Time complexity improvements needed
            
            Focus on algorithmic improvements rather than micro-optimizations.
            Keep your response concise (3-4 sentences).
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip() if response.text else None
            
        except Exception as e:
            logger.error(f"Error analyzing time limit exceeded: {str(e)}")
            return None

# Create a singleton instance
gemini_service = GeminiService()
