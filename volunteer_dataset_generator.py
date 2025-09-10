#!/usr/bin/env python3
"""
Volunteer Performance Dataset Generator
=====================================

This script generates realistic datasets for tracking volunteer performance
in student organizations. Each volunteer has tasks with marks (1-5) and 
ratings (-1 to 3) that are multiplied to get task scores.
"""

import random
import csv
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
import argparse
from datetime import datetime, timedelta

# Romanian names database
ROMANIAN_FIRST_NAMES = {
    'male': [
        'Alexandru', 'Andrei', 'Adrian', 'Bogdan', 'Catalin', 'Daniel', 'David', 
        'Eduard', 'Florin', 'Gabriel', 'George', 'Ion', 'Ionut', 'Marian', 
        'Mihai', 'Nicolae', 'Octavian', 'Paul', 'Razvan', 'Robert', 'Stefan', 
        'Teodor', 'Valentin', 'Victor', 'Vlad', 'Radu', 'Cristian', 'Liviu',
        'Marius', 'Sergiu', 'Lucian', 'Cosmin', 'Calin', 'Darius', 'Emil'
    ],
    'female': [
        'Alexandra', 'Ana', 'Andreea', 'Bianca', 'Carmen', 'Cristina', 'Dana', 
        'Elena', 'Florentina', 'Gabriela', 'Ioana', 'Laura', 'Maria', 'Monica', 
        'Nicoleta', 'Oana', 'Paula', 'Raluca', 'Roxana', 'Simona', 'Teodora', 
        'Valentina', 'Violeta', 'Diana', 'Alina', 'Adina', 'Camelia', 'Daniela',
        'Larisa', 'Mihaela', 'Ramona', 'Silvia', 'Corina', 'Denisa', 'Iulia'
    ]
}

ROMANIAN_LAST_NAMES = [
    'Popescu', 'Ionescu', 'Popa', 'Radu', 'Stoica', 'Stan', 'Dumitrescu', 
    'Gheorghiu', 'Constantin', 'Marin', 'Tudor', 'Barbu', 'Nistor', 'Florea', 
    'Georgescu', 'Cristea', 'Stanciu', 'Matei', 'Moldovan', 'Dima', 'Ilie', 
    'Andreescu', 'Marinescu', 'Petrescu', 'Vasile', 'Lungu', 'Manea', 'Ciobanu',
    'Dobre', 'Enache', 'Mihai', 'Neagu', 'Preda', 'Sandu', 'Toma', 'Vlad',
    'Mocanu', 'Rusu', 'Petre', 'Andrei', 'Badea', 'Calin', 'Filip'
]

@dataclass
class Task:
    """Represents a single task with mark and rating"""
    task_id: str
    mark: int  # 1-5
    rating: int  # -1 to 3
    score: int  # mark * rating
    task_type: str
    date_completed: str

@dataclass
class Volunteer:
    """Represents a volunteer with their tasks and total score"""
    name: str
    total_score: int
    tasks: List[Task]
    tasks_completed: int
    average_mark: float
    average_rating: float

class VolunteerDatasetGenerator:
    """Generates realistic volunteer performance datasets"""
    
    TASK_TYPES = [
        'Imagine & PR', 'Financiar', 'Resurse Umane', 
        'Tineret', 'Educational',
        'Caravana UBB', 'UBB Festival', 'FutureUp',
        'JSU', 'Mind Matters', 'Exchange National',
        'Exchange International'
    ]
    
    def __init__(self, seed: int = None):
        """Initialize the generator with optional random seed"""
        if seed:
            random.seed(seed)
    
    def generate_romanian_name(self) -> str:
        """Generate a realistic Romanian name"""
        gender = random.choice(['male', 'female'])
        first_name = random.choice(ROMANIAN_FIRST_NAMES[gender])
        last_name = random.choice(ROMANIAN_LAST_NAMES)
        return f"{first_name} {last_name}"
    
    def generate_task(self, volunteer_profile: str, task_id: str) -> Task:
        """Generate a single task based on volunteer profile"""
        # Adjust probabilities based on volunteer profile
        if volunteer_profile == 'high_performer':
            mark_weights = [0.05, 0.10, 0.25, 0.35, 0.25]  # Favors 4-5
            rating_weights = [0.05, 0.10, 0.20, 0.35, 0.30]  # Favors 2-3
        elif volunteer_profile == 'low_performer':
            mark_weights = [0.30, 0.35, 0.25, 0.08, 0.02]  # Favors 1-2
            rating_weights = [0.25, 0.35, 0.25, 0.10, 0.05]  # Favors -1 to 1
        else:  # average_performer
            mark_weights = [0.10, 0.20, 0.40, 0.20, 0.10]  # Normal distribution
            rating_weights = [0.10, 0.15, 0.30, 0.30, 0.15]  # Normal distribution
        
        mark = random.choices([1, 2, 3, 4, 5], weights=mark_weights)[0]
        rating = random.choices([-1, 0, 1, 2, 3], weights=rating_weights)[0]
        score = mark * rating
        task_type = random.choice(self.TASK_TYPES)
        
        # Generate realistic date within last 6 months
        days_ago = random.randint(1, 180)
        date_completed = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        return Task(
            task_id=task_id,
            mark=mark,
            rating=rating,
            score=score,
            task_type=task_type,
            date_completed=date_completed
        )
    
    def determine_volunteer_profile(self, distribution: Dict[str, float]) -> str:
        """Determine volunteer profile based on distribution"""
        profiles = list(distribution.keys())
        weights = list(distribution.values())
        return random.choices(profiles, weights=weights)[0]
    
    def generate_volunteer(self, distribution: Dict[str, float], 
                         task_range: Tuple[int, int]) -> Volunteer:
        """Generate a single volunteer with realistic data"""
        name = self.generate_romanian_name()
        profile = self.determine_volunteer_profile(distribution)
        
        # Generate number of tasks based on profile
        min_tasks, max_tasks = task_range
        if profile == 'high_performer':
            num_tasks = random.randint(max(min_tasks, max_tasks // 2), max_tasks)
        elif profile == 'low_performer':
            num_tasks = random.randint(min_tasks, max(min_tasks + 1, max_tasks // 2))
        else:
            num_tasks = random.randint(min_tasks, max_tasks)
        
        # Generate tasks
        tasks = []
        for i in range(num_tasks):
            task_id = f"T{i+1:03d}"
            task = self.generate_task(profile, task_id)
            tasks.append(task)
        
        # Calculate metrics
        total_score = sum(task.score for task in tasks)
        average_mark = sum(task.mark for task in tasks) / len(tasks)
        average_rating = sum(task.rating for task in tasks) / len(tasks)
        
        return Volunteer(
            name=name,
            total_score=total_score,
            tasks=tasks,
            tasks_completed=len(tasks),
            average_mark=round(average_mark, 2),
            average_rating=round(average_rating, 2)
        )
    
    def generate_dataset(self, 
                        dataset_size: int,
                        distribution: Dict[str, float] = None,
                        task_range: Tuple[int, int] = (3, 15),
                        output_format: str = 'csv') -> List[Volunteer]:
        """Generate complete dataset"""
        if distribution is None:
            distribution = {
                'high_performer': 0.20,
                'average_performer': 0.60,
                'low_performer': 0.20
            }
        
        # Validate distribution
        if abs(sum(distribution.values()) - 1.0) > 0.01:
            raise ValueError("Distribution weights must sum to 1.0")
        
        volunteers = []
        for i in range(dataset_size):
            volunteer = self.generate_volunteer(distribution, task_range)
            volunteers.append(volunteer)
        
        return volunteers
    
    def save_to_csv(self, volunteers: List[Volunteer], filename: str):
        """Save dataset to CSV file"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Total_Score', 'Tasks_Completed', 'Average_Mark', 
                         'Average_Rating']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for volunteer in volunteers:
                writer.writerow({
                    'Name': volunteer.name,
                    'Total_Score': volunteer.total_score,
                    'Tasks_Completed': volunteer.tasks_completed,
                    'Average_Mark': volunteer.average_mark,
                    'Average_Rating': volunteer.average_rating
                })
    
    def save_detailed_to_json(self, volunteers: List[Volunteer], filename: str):
        """Save detailed dataset with all tasks to JSON file"""
        data = [asdict(volunteer) for volunteer in volunteers]
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
    
    def print_statistics(self, volunteers: List[Volunteer]):
        """Print dataset statistics"""
        total_volunteers = len(volunteers)
        score_sum = 0
        task_sum = 0
        mark_sum = 0
        rating_sum = 0
        
        for volunteer in volunteers:
            score_sum += volunteer.total_score
            task_sum += volunteer.tasks_completed
            mark_sum += volunteer.average_mark
            rating_sum += volunteer.average_rating
        
        print(f"\n=== Dataset Statistics ===")
        print(f"Total Volunteers: {total_volunteers}")
        print(f"Average Score: {score_sum / total_volunteers:.2f}")
        print(f"Average Tasks per Volunteer: {task_sum / total_volunteers:.2f}")
        print(f"Average Mark: {mark_sum / total_volunteers:.2f}")
        print(f"Average Rating: {rating_sum / total_volunteers:.2f}")
        
        # Score distribution
        scores = [v.total_score for v in volunteers]
        print(f"Score Range: {min(scores)} - {max(scores)}")

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description='Generate volunteer performance dataset')
    parser.add_argument('--size', type=int, default=50, 
                       help='Number of volunteers to generate (default: 50)')
    parser.add_argument('--high-performers', type=float, default=0.20,
                       help='Percentage of high performers (default: 0.20)')
    parser.add_argument('--low-performers', type=float, default=0.20,
                       help='Percentage of low performers (default: 0.20)')
    parser.add_argument('--min-tasks', type=int, default=3,
                       help='Minimum tasks per volunteer (default: 3)')
    parser.add_argument('--max-tasks', type=int, default=15,
                       help='Maximum tasks per volunteer (default: 15)')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    parser.add_argument('--output', type=str, default='volunteers',
                       help='Output filename prefix (default: volunteers)')
    parser.add_argument('--detailed', action='store_true',
                       help='Also generate detailed JSON with all tasks')
    
    args = parser.parse_args()
    
    # Calculate distribution
    high_perf = args.high_performers
    low_perf = args.low_performers
    avg_perf = 1.0 - high_perf - low_perf
    
    if avg_perf < 0:
        print("Error: High and low performer percentages sum to more than 1.0")
        return
    
    distribution = {
        'high_performer': high_perf,
        'average_performer': avg_perf,
        'low_performer': low_perf
    }
    
    # Generate dataset
    generator = VolunteerDatasetGenerator(seed=args.seed)
    volunteers = generator.generate_dataset(
        dataset_size=args.size,
        distribution=distribution,
        task_range=(args.min_tasks, args.max_tasks)
    )
    
    # Save files
    csv_filename = f"{args.output}.csv"
    generator.save_to_csv(volunteers, csv_filename)
    print(f"Dataset saved to {csv_filename}")
    
    if args.detailed:
        json_filename = f"{args.output}_detailed.json"
        generator.save_detailed_to_json(volunteers, json_filename)
        print(f"Detailed dataset saved to {json_filename}")
    
    # Print statistics
    generator.print_statistics(volunteers)

if __name__ == "__main__":
    main()
