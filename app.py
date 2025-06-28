"""
🧱 Prompt Brickz Flask Application

Main Flask app that serves the frontend and provides API endpoints
for the Prompt Brickz prompt engineering system.
"""

import os
import asyncio
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Brickz modules
from brickz.wizard import BrickzWizard
from brickz.bricks import BrickLibrary, BrickCategory
from brickz.optimizer import optimize_content, get_optimization_info

app = Flask(__name__, static_folder='frontend', template_folder='frontend')
CORS(app)

# Initialize Brickz components
wizard = BrickzWizard()
brick_library = BrickLibrary()

@app.route('/')
def index():
    """Serve the main Brickz interface"""
    return send_from_directory('frontend', 'index.html')

@app.route('/api/wizard/greet')
def wizard_greet():
    """Get wizard greeting"""
    return jsonify({
        'message': wizard.greet_user(),
        'status': 'ready'
    })

@app.route('/api/wizard/analyze', methods=['POST'])
def wizard_analyze():
    """Analyze content and get wizard suggestions"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        content_type = data.get('content_type', 'auto')
        
        if not content.strip():
            return jsonify({
                'error': 'No content provided',
                'message': wizard.create_wizard_response('help_needed')
            }), 400
        
        # Analyze content
        analysis = wizard.analyze_content(content, content_type)
        
        return jsonify({
            'analysis': {
                'content_type': analysis.content_type,
                'suggested_template': analysis.suggested_template,
                'confidence': analysis.confidence,
                'suggested_bricks': analysis.suggested_bricks,
                'reasoning': analysis.reasoning
            },
            'wizard_comment': analysis.wizard_comment,
            'status': 'analyzed'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': wizard.create_wizard_response('error_occurred')
        }), 500

@app.route('/api/bricks/categories')
def get_brick_categories():
    """Get all brick categories and their bricks"""
    try:
        workpath = request.args.get('workpath', 'coding')
        categories = brick_library.get_bricks_for_workpath(workpath)
        
        # Convert to frontend format
        result = {}
        for category_key, bricks in categories.items():
            result[category_key] = [
                {
                    'id': brick.id,
                    'name': brick.name,
                    'description': brick.description,
                    'color': brick.category.color,
                    'is_custom': brick.is_custom
                }
                for brick in bricks
            ]
        
        return jsonify({
            'categories': result,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/bricks/create', methods=['POST'])
def create_custom_brick():
    """Create a new custom brick"""
    try:
        data = request.get_json()
        
        name = data.get('name', '').strip()
        category_key = data.get('category', '')
        description = data.get('description', '').strip()
        modifier_text = data.get('modifier_text', '').strip()
        workpaths = data.get('workpaths', ['coding'])
        
        # Validate input
        if not all([name, category_key, description, modifier_text]):
            return jsonify({
                'error': 'All fields are required',
                'message': wizard.create_wizard_response('help_needed')
            }), 400
        
        # Get category enum
        try:
            category = next(cat for cat in BrickCategory if cat.key == category_key)
        except StopIteration:
            return jsonify({
                'error': f'Invalid category: {category_key}',
                'message': wizard.create_wizard_response('error_occurred')
            }), 400
        
        # Validate brick
        is_valid, validation_message = brick_library.validate_custom_brick(name, category, modifier_text)
        if not is_valid:
            return jsonify({
                'error': validation_message,
                'message': wizard.create_wizard_response('error_occurred')
            }), 400
        
        # Create the brick
        brick = brick_library.create_custom_brick(
            name=name,
            category=category,
            description=description,
            modifier_text=modifier_text,
            workpaths=workpaths,
            creator='user'
        )
        
        return jsonify({
            'brick': {
                'id': brick.id,
                'name': brick.name,
                'description': brick.description,
                'color': brick.category.color,
                'is_custom': brick.is_custom
            },
            'message': wizard.create_wizard_response('brick_created', brick_name=name),
            'status': 'created'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': wizard.create_wizard_response('error_occurred')
        }), 500

@app.route('/api/optimize', methods=['POST'])
def optimize_prompt():
    """Optimize a prompt using selected bricks (two-pass optimization)"""
    try:
        data = request.get_json()
        
        content = data.get('content', '').strip()
        workpath = data.get('workpath', 'coding')
        selected_brick_ids = data.get('selected_bricks', {})
        user_context = data.get('user_context', '')
        
        if not content:
            return jsonify({
                'error': 'No content provided',
                'message': wizard.create_wizard_response('help_needed')
            }), 400
        
        # Convert brick IDs to brick objects
        selected_bricks = {}
        for category, brick_id in selected_brick_ids.items():
            brick = brick_library.get_brick(brick_id)
            if brick:
                selected_bricks[category] = brick
                # Increment usage count
                brick_library.increment_usage(brick_id)
        
        # Run two-pass optimization
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            optimized_result = loop.run_until_complete(
                optimize_content(content, workpath, selected_bricks, user_context)
            )
        finally:
            loop.close()
        
        return jsonify({
            'optimized_prompt': optimized_result,
            'message': wizard.create_wizard_response('optimization_complete'),
            'optimization_info': get_optimization_info(),
            'status': 'optimized'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': wizard.create_wizard_response('error_occurred')
        }), 500

@app.route('/api/mad-libs/<category>')
def get_mad_libs_prompts(category):
    """Get Mad Libs style prompts for custom brick creation"""
    try:
        category_enum = next(cat for cat in BrickCategory if cat.key == category)
        prompts = brick_library.get_mad_libs_prompts(category_enum)
        
        return jsonify({
            'prompts': prompts,
            'category': category,
            'status': 'success'
        })
        
    except StopIteration:
        return jsonify({
            'error': f'Invalid category: {category}',
            'status': 'error'
        }), 400
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/bricks/search')
def search_bricks():
    """Search bricks by query"""
    try:
        query = request.args.get('q', '')
        workpath = request.args.get('workpath', None)
        
        if not query:
            return jsonify({
                'results': [],
                'status': 'success'
            })
        
        results = brick_library.search_bricks(query, workpath)
        
        brick_results = [
            {
                'id': brick.id,
                'name': brick.name,
                'description': brick.description,
                'category': brick.category.key,
                'color': brick.category.color,
                'is_custom': brick.is_custom
            }
            for brick in results
        ]
        
        return jsonify({
            'results': brick_results,
            'query': query,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get application statistics"""
    try:
        popular_bricks = brick_library.get_popular_bricks(5)
        
        return jsonify({
            'stats': {
                'total_bricks': len(brick_library.bricks),
                'custom_bricks': len([b for b in brick_library.bricks.values() if b.is_custom]),
                'popular_bricks': [
                    {
                        'name': brick.name,
                        'category': brick.category.key,
                        'usage_count': brick.usage_count
                    }
                    for brick in popular_bricks
                ]
            },
            'optimization_info': get_optimization_info(),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': wizard.create_wizard_response('help_needed')
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': wizard.create_wizard_response('error_occurred')
    }), 500

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Run the app
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5001))  # Changed to 5001 to avoid conflicts
    
    print("🧱 Starting Prompt Brickz Application...")
    print(f"🚀 Server running at http://localhost:{port}")
    print("🧙‍♂️ TARS-inspired wizard ready for magical optimization!")
    print("✨ Two-pass PSE enhancement active for 150% better results")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
