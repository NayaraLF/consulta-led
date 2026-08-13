"""
Dummy entrypoint for Vercel static site.
This file exists only to satisfy Vercel's Python runtime detection.
The actual content is served from the 'public' directory.
"""

def handler(request):
    return {
        'statusCode': 404,
        'body': 'Not Found - Please use the static site instead'
    }
