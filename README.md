# Volunteer Performance Dataset Generator

Generate realistic volunteer performance datasets and analyze promotion criteria for student organizations.

## Quick Setup

```bash
# Create environment
uv venv --python=python3.12

# Activate environment
source .venv/bin/activate  # macOS/Linux
# or .venv\Scripts\activate  # Windows

# Install dependencies
uv sync
```

## How It Works

Volunteers complete tasks that are scored based on:
- **Mark** (1-5): Task difficulty/importance
- **Rating** (-1 to 3): Performance quality
- **Total Score**: Sum of all (Mark × Rating) scores

## Quick Start

### Option 1: Interactive Notebook (Recommended)
```bash
jupyter notebook volunteer_analysis_notebook.ipynb
```
Complete workflow with visualizations and step-by-step analysis.

### Option 2: Command Line
```bash
# Generate dataset
python volunteer_dataset_generator.py --size 50

# Analyze for promotion criteria
python volunteer_analyzer.py volunteers.csv
```

## Common Usage Examples

```bash
# Generate larger dataset
python volunteer_dataset_generator.py --size 100

# Analyze top 25% instead of default 10%
python volunteer_analyzer.py volunteers.csv --percentile 25

# Focus on positive scores only (score >= 0)
python volunteer_analyzer.py volunteers.csv --above 0
```

## CLI Arguments

### Generator (`volunteer_dataset_generator.py`)
- `--size N`: Number of volunteers (default: 50)
- `--high-performers RATIO`: Percentage of high performers (default: 0.20)
- `--low-performers RATIO`: Percentage of low performers (default: 0.20)
- `--min-tasks N`: Minimum tasks per volunteer (default: 3)
- `--max-tasks N`: Maximum tasks per volunteer (default: 15)
- `--seed N`: Random seed for reproducibility
- `--output NAME`: Output filename prefix (default: volunteers)
- `--detailed`: Generate detailed JSON with all task information

### Analyzer (`volunteer_analyzer.py`)
- `dataset`: Dataset file to analyze (default: volunteers.csv)
- `--json`: Treat the dataset file as JSON instead of CSV
- `--above SCORE`: Analyze only volunteers with total scores >= SCORE
- `--percentile PCT`: Target percentile for promotion (e.g., 10.0 for top 10%) (default: 10.0)
- `--method {percentile,median,mean}`: Method for setting thresholds (default: percentile)
- `--compare-methods`: Compare all three methods (percentile, median, mean) side by side

## Volunteer Profiles

### High Performers (Default 20%)
- Higher marks (tend toward 4-5)
- Better ratings (tend toward 2-3)
- More tasks completed
- Realistic total scores: 40-150+

### Average Performers (Default 60%)
- Balanced marks (centered around 3)
- Balanced ratings (centered around 1-2)
- Moderate task completion
- Realistic total scores: 10-60

### Low Performers (Default 20%)
- Lower marks (tend toward 1-2)
- Lower ratings (tend toward -1 to 1)
- Fewer tasks completed
- Realistic total scores: -20 to 30

## Output Formats

### CSV Output
Simple summary with columns:
- Name (Romanian names)
- Total_Score
- Tasks_Completed  
- Average_Mark
- Average_Rating
- Join_Date
- Status

### JSON Output (--detailed)
Complete data including all individual tasks with:
- Task details (mark, rating, score, type, date)
- Full volunteer profiles
- All calculated metrics

## Programming Interface

```python
from volunteer_dataset_generator import VolunteerDatasetGenerator

# Create generator
generator = VolunteerDatasetGenerator(seed=42)

# Generate custom dataset
volunteers = generator.generate_dataset(
    dataset_size=50,
    distribution={
        'high_performer': 0.25,
        'average_performer': 0.50, 
        'low_performer': 0.25
    },
    task_range=(5, 15)
)

# Save results
generator.save_to_csv(volunteers, "my_dataset.csv")
generator.save_detailed_to_json(volunteers, "detailed.json")
generator.print_statistics(volunteers)
```

## What You Get

### Dataset Output
- **CSV**: Summary with names, scores, and basic metrics
- **JSON**: Detailed data including individual task information

### Analysis Results
- Performance statistics and percentiles
- Promotion criteria suggestions (top 10%, 25%, etc.)
- Comparison of different threshold methods
- Filtering options for targeted analysis

## Additional Notes

- **Romanian names**: Includes 70+ authentic Romanian first names and 40+ surnames
- **Reproducible**: Use `--seed` parameter for consistent results  
- **Use cases**: Testing promotion algorithms, dashboard development, ML training data
- **Documentation**: See `ANALIZA.md` for detailed analysis methodology (in Romanian)

## Interactive Notebook

The `volunteer_analysis_notebook.ipynb` combines dataset generation and analysis with interactive visualizations.

### What it provides:
- **Visual analysis**: Charts and graphs for data exploration
- **Step-by-step workflow**: Generate data → analyze → set promotion criteria
- **Interactive testing**: Try different percentile targets and see results instantly
- **Export capabilities**: Save analysis results and top performer lists

### Getting started:
```bash
# Launch the notebook
jupyter notebook volunteer_analysis_notebook.ipynb
```

The notebook walks you through:
1. **Dataset generation** with customizable parameters
2. **Statistical analysis** with visualizations  
3. **Promotion criteria testing** with different methods
4. **Results export** for organizational use

## Tips for Promotion Criteria Analysis

- **Start with percentile method** for traditional, ranking-based approach
- **Use median method** for stable criteria that resist outliers
- **Try mean method** for performance-driven organizations
- **Compare methods** with `--compare-methods` to see all options
- **Adjust percentile targets** based on your organization's selectivity needs:
  - **5-10%**: Highly selective (elite performers only)
  - **15-25%**: Moderate selectivity (balanced approach)
  - **30-50%**: Inclusive (broader recognition)
- **Combine with score filtering** (`--above`) to focus on specific performance ranges
- **Test different combinations** to find what works best for your organization
