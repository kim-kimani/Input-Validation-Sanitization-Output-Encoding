import json
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.html import escape
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import connection
from .models import Employee, Subscriber

from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'sandbox.html')

def report(request):
    return render(request, 'report.html')

@csrf_exempt
def api_html_encode(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            raw_input = data.get('input', '')
            encoded = escape(raw_input)
            return JsonResponse({'status': 'success', 'encoded': encoded, 'raw': raw_input})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)

@csrf_exempt
def api_sql_search(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            search_term = data.get('term', '')
            query_type = data.get('type', 'safe')

            results = []
            if query_type == 'raw':
                import sqlparse
                with connection.cursor() as cursor:
                    query = search_term
                    try:
                        statements = sqlparse.split(query)
                        for stmt in statements:
                            stmt = stmt.strip()
                            if not stmt:
                                continue
                            cursor.execute(stmt)
                            if cursor.description:
                                columns = [col[0] for col in cursor.description]
                                rows = cursor.fetchall()
                                for row in rows:
                                    results.append(dict(zip(columns, row)))
                    except Exception as e:
                        return JsonResponse({'status': 'error', 'message': str(e), 'query': query})
                return JsonResponse({'status': 'success', 'results': results, 'query': query})
                
            elif query_type == 'vulnerable':
                import sqlparse
                # Vulnerable SQL execution
                with connection.cursor() as cursor:
                    query = f"SELECT id, name, department, salary FROM sandbox_employee WHERE name = '{search_term}'"
                    try:
                        statements = sqlparse.split(query)
                        for stmt in statements:
                            stmt = stmt.strip()
                            if not stmt:
                                continue
                            cursor.execute(stmt)
                            if cursor.description:
                                columns = [col[0] for col in cursor.description]
                                rows = cursor.fetchall()
                                for row in rows:
                                    results.append(dict(zip(columns, row)))
                    except Exception as e:
                        return JsonResponse({'status': 'error', 'message': str(e), 'query': query})
                return JsonResponse({'status': 'success', 'results': results, 'query': query})
            else:
                # Safe SQL execution
                query = "SELECT id, name, department, salary FROM sandbox_employee WHERE name = %s"
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(query, [search_term])
                        rows = cursor.fetchall()
                        for row in rows:
                            results.append({'id': row[0], 'name': row[1], 'department': row[2], 'salary': row[3]})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e), 'query': query})
                return JsonResponse({'status': 'success', 'results': results, 'query': query})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)

@csrf_exempt
def api_subscribe(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '')
            validate_only = data.get('validate_only', False)
            
            try:
                validate_email(email)
            except ValidationError as e:
                return JsonResponse({'status': 'error', 'message': e.message})
                
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'Email already subscribed.'})
                
            if validate_only:
                return JsonResponse({'status': 'success', 'message': 'Email format is valid and available.'})
                
            Subscriber.objects.create(email=email)
            return JsonResponse({'status': 'success', 'message': 'Successfully subscribed!'})
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)
