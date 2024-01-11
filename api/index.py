from flask import Flask, request
import json
import os
from supabase import create_client, Client

app = Flask(__name__)
if __name__ == "__main__":                                              
    app.run(host='0.0.0.0', port=5000,workers=4)

url="https://frbmnrbtdefdfndosvjj.supabase.co"
key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZyYm1ucmJ0ZGVmZGZuZG9zdmpqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDIzNzE1MTQsImV4cCI6MjAxNzk0NzUxNH0.RNy8yeRQmVLahLW2iO8HyA-fn9iQevTDBzSHIMgkhms'
supabase: Client = create_client(url, key)
# Configure the upload set and the upload folder


####################################################User functions#########################################################
#sign up 
@app.route('/users.signup',methods=['GET','POST'])
def api_users_signup():
    email= request.form.get('email')
    fullname= request.form.get('fullname')
    password= request.form.get('password')
    phonenum= request.form.get('phonenum')
    profile_pic=request.form.get('profile_pic')
    error =False
    if (not email) or (len(email)<5): #You can even check with regx
        error='Email needs to be valid'
    if (not error) and ( (not password) or (len(password)<5) ):
        error='Provide a password'        
    if (not error):
        response = supabase.table('USERS').select("*").ilike('email', email).execute()
        if len(response.data)>0:    
            error='User already exists'
    if (not error):
        #photo_path = os.path.join(app.config["UPLOADED_PHOTOS_DEST"], photos.save(profile_pic))    
        response = supabase.table('USERS').insert(
            {"email": email, 
            "password": password,
            "fullname":fullname,
            "phonenum":phonenum,
            'profile_pic':profile_pic,
            }).execute()
        print(str(response.data))
        if len(response.data)==0:
            error='Error creating the user'        
    if error:
        return json.dumps({'status':500,'message':error})        
    
    return json.dumps({'status':200,'message':'','data':response.data[0]})

#login 
@app.route('/users.login',methods=['GET','POST'])
def api_users_login():
    email= request.form.get('email')
    password= request.form.get('password')
    error =False
    if (not email): #You can even check with regx
        error='Email needs to be valid'
    if (not error) and ( (not password) ):
        error='Provide a password'        
    if (not error):    
        response = supabase.table('USERS').select("*").ilike('email', email).eq('password',password).execute()
        if len(response.data)>0:
            return json.dumps({'status':200,'message':'','data':response.data[0]})
               
    if not error:
         error='Invalid Email or password'        
    
    return json.dumps({'status':500,'message':error})        
    
#auth 
@app.route('/users.signup.auth',methods=['GET','POST'])
def api_users_signup_auth():
    email= request.args.get('email')
    password= request.args.get('password')
    response = supabase.auth.sign_up({"email": email, "password": password})        
    print(str(response))    
    return str(response)
#show user info in the profile 
@app.route('/user.profile',methods=['GET','POST'])
def api_user_profile(): 
    id_user= request.form.get('id_user')
    response = supabase.table('USERS').select("*").eq('id',id_user).limit(1).execute()  
    return json.dumps({'status':200,'message':'profile data fetched ','data':response.data})

#update profile 
#display requests on user posts 
#############################################Products functions ###############################################
#fetch products
@app.route('/product.all',methods=['GET','POST'])
def api_fetch_products(): 
    response = supabase.table('POST').select("*").execute()  
    return json.dumps({'status':200,'message':'Post uploaded','data':response.data})

#add product
@app.route('/product.add', methods=['POST','GET'])
def api_product_add():
    id_user= request.form.get('id_user')
    description= request.form.get('description')
    price=request.form.get('price')
    category=request.form.get('category')
    name=request.form.get('name')
    location=request.form.get('location')
    error =False        
    if (not error):
        response = supabase.table('POST').insert({
            "user_id": id_user,
            "Description": description,
            "price": price,
            "category_id": category,
            "name": name,
            "location": location
        }).execute()
        if len(response.data)>0:
            return json.dumps({'status':200,'message':'','data':response.data})
               
    if not error:
         error='Invalid info'        
    
    return json.dumps({'status':500,'message':error})
#add product images 
@app.route('/product.images', methods=['POST'])
def api_product_add_images():
    post_id= request.form.get('post_id')
    profile_image=request.form.get('image')
    error =False        
    if (not error):
        response = supabase.table('post_image').insert({
            "post_id": post_id,
            "image": profile_image,
        }).execute()
        if len(response.data)>0:
            return json.dumps({'status':200,'message':'','data':response.data})            
    else:
        error='Invalid info'        
    
    return json.dumps({'status':500,'message':error})
#fetch categories 
@app.route('/categories.all',methods=['GET'])
def api_fetch_categories(): 
    response = supabase.table('categories').select("*").execute()  
    return json.dumps({'status':200,'message':'data fetched','data':response.data})

#fetch products by categories 
@app.route('/product.by_category', methods=['GET','POST'])
def api_fetch_products_by_category():
    category_id = request.form.get('category_id')

    if not category_id:
        return json.dumps({'status': 400, 'message': 'Category ID is required'})

    try:
        # Assuming 'category_id' is the foreign key in the 'POST' table
        response = supabase.table('POST').select("*").eq('category_id', category_id).execute()

        return json.dumps({'status': 200, 'message': 'Products fetched by category', 'data': response.data})
    except Exception as e:
        return json.dumps({'status': 500, 'message': 'Error fetching products by category', 'error': str(e)})

######################################Product and user ###################################
#display user posts 
@app.route('/product.user',methods=['GET','POST'])
def api_user_products(): 
    id_user = request.form.get('id_user')
    error = False

    if not id_user:
        error = 'User ID is required'

    if not error:
        try:
            response = supabase.table('POST').select("*").eq('user_id', id_user).execute()
            return json.dumps({'status': 200, 'message': 'User posts fetched', 'data': response.data})
        except Exception as e:
            return json.dumps({'status': 500, 'message': 'Error fetching user posts', 'error': str(e)})

    return json.dumps({'status': 500, 'message': error})

#display user rents 

######################Request to rent ########################
@app.route('/product.request',methods=['GET','POST'])
def api_user_request(): 
    id_user = request.form.get('id_user')
    id_post= request.form.get('id_post')
    error = False
    if not id_user  and not id_post :
        error = 'User ID and post ID  are required'

    if not error:
        try:
            response = supabase.table('Bookings').insert({
            "user_id": id_user,
            "post_id": id_post,
            "status": "pending",
        }).execute()
            return json.dumps({'status': 200, 'message': 'Request sent', 'data': response.data})
        except Exception as e:
            return json.dumps({'status': 500, 'message': 'Error sending user request', 'error': str(e)})

    return json.dumps({'status': 500, 'message': error})

@app.route('/product.requests_count', methods=['GET', 'POST'])
def api_requests_count():
    try:
        response = supabase.table('Bookings').select('*').execute()
        for i in response.data:
            print(i['post_id'])
        return json.dumps({'status': 200, 'message': 'Requests count fetched', 'data': response.data})
    except Exception as e:
        return json.dumps({'status': 500, 'message': 'Error fetching requests count', 'error': str(e)})

@app.route('/')
def about():
    return 'Welcome ENSIA Students'

