import openai
from typing import List, Dict, Any

class SolutionValidator:
    def __init__(self, config: Dict[str, Any]):
        self.client = openai.OpenAI(api_key=config['openai_key'])
    
    def validate_solution(self, solution: Dict[str, Any]) -> float:
        prompt = f"""
        You are a task validator. Rate the quality of this solution on a scale of 1-5, where:
        1 = Poor/Incomplete
        2 = Basic
        3 = Satisfactory
        4 = Good
        5 = Excellent

        Task: {solution['task']}
        Solution: {solution['solution']}

        Return only a number between 1 and 5.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=10
        )
        
        try:
            score = float(response.choices[0].message.content.strip())
            return min(max(score, 1), 5)  # Ensure score is between 1-5
        except ValueError:
            return 1  # Default to lowest score if parsing fails
    
    def validate(self, input_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not input_data:
            return {"passed": False, "average_score": 0, "scores": []}
        
        scores = [self.validate_solution(solution) for solution in input_data]
        print(f"Scores: {scores}")
        average_score = sum(scores) / len(scores) / 5
        passing_threshold = 0.6
        individual_threshold = 0.8
        
        all_scores_pass = all(score >= individual_threshold for score in scores)
        average_passes = average_score >= passing_threshold
        
        print(f"All scores pass: {all_scores_pass}, Average passes: {average_passes}")
        return {
            "passed": all_scores_pass and average_passes,
            "average_score": round(average_score, 2),
            "scores": scores,
            "details": {
                "all_scores_pass": all_scores_pass,
                "average_passes": average_passes
            }
        }

