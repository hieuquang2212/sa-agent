from flask import Flask, jsonify, request
from pydantic import BaseModel, ValidationError
# from agents.ba_agents import create_ba_agent
from architect import SolutionCrew
from analyst_requirement import AnalystBusinessCrew
from textwrap import dedent
from utils.helpers import print_weights_nicely
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from crewai import Task, Crew
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class WeightDTO(BaseModel):
    operationalExcellence: int
    security: int
    reliability: int
    performanceEfficiency: int
    costOptimization: int
    sustainability: int

class BodyDTO(BaseModel):
    problem: str
    cloudProvider: str
    aiModel: str
    weights: WeightDTO

@app.route('/api/solve', methods=['POST'])
def get_users():
    try:
        data = BodyDTO(**request.json)
        input_weights = data.weights
        # file = request.files['file']
        # filename = secure_filename(file.filename)
        # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # file.save(filepath)

        weights = {
            "operational_excellence": float(input_weights.operationalExcellence) / 100,
            "security": float(input_weights.security) / 100,
            "reliability": float(input_weights.reliability) / 100,
            "performance_efficiency": float(input_weights.performanceEfficiency) / 100,
            "cost_optimization": float(input_weights.costOptimization) / 100,
            "sustainability": float(input_weights.sustainability) / 100
        }
        
        # baCrew = AnalystBusinessCrew(
        #         filepath,
        #         data.cloudProvider,
        #         data.aiModel,
        #         openai_api_key=os.getenv("OPENAI_API_KEY"),
        #         anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        #         serper_api_key=os.getenv("SERPER_API_KEY"))
        
        # description_problem = baCrew.run()

        if data.cloudProvider == "AWS":
            from agents.aws_agents import AWSAgents
            from tasks.aws_tasks import AWSTasks    
            crew = SolutionCrew(
                                # description_problem,
                                data.problem,
                                weights,
                                data.cloudProvider,
                                data.aiModel,
                                openai_api_key=os.getenv("OPENAI_API_KEY"),
                                anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
                                serper_api_key=os.getenv("SERPER_API_KEY"))
        else:
            print("Invalid cloud provider. Please select AWS, Azure, or GCP.")
            exit(1)

        result = crew.run()
        return jsonify({
            "result": result.dict()
        })

    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

if __name__ == '__main__':
    app.run(debug=True)