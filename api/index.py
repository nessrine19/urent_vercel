from flask import Flask, request
import json
import os
from datetime import datetime
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
            "created_at":datetime.now().isoformat()
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
#user info by id 
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
            "location": location,
            "created_at":datetime.now().isoformat()
        }).execute()
        if len(response.data)>0:
            return json.dumps({'status':200,'message':'','data':response.data})
               
    if not error:
         error='Invalid info'        
    
    return json.dumps({'status':500,'message':error})
#add product images 
@app.route('/product.images', methods=['POST','GET'])
def api_product_add_images():
    post_id= request.form.get('post_id')
    profile_image=request.form.get('image')
    error =False        
    if (not error):
        response = supabase.table('post_image').insert({
            "post_id": post_id,
            "image": profile_image,
            "created_at":datetime.now().isoformat()
        }).execute()
        if len(response.data)>0:
            return json.dumps({'status':200,'message':'','data':response.data})            
    else:
        error='Invalid info'        
    
    return json.dumps({'status':500,'message':error})
#fetch product's images 
@app.route('/product.get.images',methods=['GET','POST'])
def api_product_get_image(): 
    post_id= request.form.get('post_id')
    response = supabase.table('post_image').select("*").eq('post_id',post_id).execute()  
    return json.dumps({'status':200,'message':'images  fetched ','data':response.data})
#post likes
@app.route('/product.like',methods=['GET','POST'])
def api_product_like(): 
    id_user = request.form.get('id_user')
    id_post= request.form.get('id_post')
    error = False
    if not id_user  and not id_post :
        error = 'User ID and post ID  are required'

    if not error:
        try:
            response = supabase.table('likes').insert({
            "user_id": id_user,
            "post_id": id_post,
            "created_at":datetime.now().isoformat()
        }).execute()
            return json.dumps({'status': 200, 'message': 'like sent', 'data': response.data})
        except Exception as e:
            return json.dumps({'status': 500, 'message': 'Error sending the like', 'error': str(e)})

    return json.dumps({'status': 500, 'message': error}) 

@app.route('/product.unlike', methods=['DELETE'])
def delete_product_like():
    id_user = request.form.get('id_user')
    id_post = request.form.get('id_post')
    error = False
    if not id_user or not id_post:
        error = 'User ID and post ID are required'

    if not error:
        try:
            # Assuming 'likes' table has columns 'user_id' and 'post_id'
            response = supabase.table('likes').delete().eq('user_id', id_user).eq('post_id', id_post).execute()
            return json.dumps({'status': 200, 'message': 'like deleted', 'data': response.data})
        except Exception as e:
            return json.dumps({'status': 500, 'message': 'Error deleting the like', 'error': str(e)})

    return json.dumps({'status': 500, 'message': error})
#fetch liked per user 
@app.route('/user.favorite',methods=['GET','POST'])
def api_uset_favorite(): 
    id_user = request.form.get('id_user')
    error = False
    if not error:
        try:
            # Use a LEFT JOIN to get all posts and whether they are liked by the specified user
            query = f"""
                SELECT POST.*, likes.user_id AS is_liked
                FROM POST
                LEFT JOIN likes ON POST.id = likes.post_id AND likes.user_id = '{id_user}';
            """

            # Execute the query
            response = supabase.query(query)

            # Check for errors in the response
            if response['error']:
                return json.dumps({"status": 500, "message": "Error fetching favorite posts", "error": response['error']['message']})

            # Get the result data
            favorite_posts = response['data']

            return json.dumps({"status": 200, "message": "Favorite posts fetched", "data": favorite_posts})

        except Exception as e:
            return json.dumps({"status": 500, "message": "Error fetching favorite posts", "error": str(e)})


#fetch top liked posts 
@app.route('/product.likes.count',methods=['GET','POST'])
def api_fetch_likes_count():
    try:
        # Fetch likes data from the 'likes' table
        likes_response = supabase.table('likes').select("*").execute()

        # Check if the response is successful
        if len(likes_response.data)>0:
            likes_data = likes_response.data

            # Create a dictionary to store post_id and corresponding like count
            like_count_dict = {}

            # Iterate through likes data and count likes for each post_id
            for like in likes_data:
                post_id = like.get('post_id')
                
                # Check if post_id is present in the dictionary, if not, initialize it
                if post_id not in like_count_dict:
                    like_count_dict[post_id] = 1
                else:
                    like_count_dict[post_id] += 1

            # Convert the dictionary to a list of dictionaries for response formatting
            result_list = [{'post_id': post_id, 'count': count} for post_id, count in like_count_dict.items()]

            # Sort the result list in descending order based on the like count
            result_list.sort(key=lambda x: x['count'], reverse=True)

            return json.dumps({'status': 200, 'message': 'Likes count fetched', 'data': result_list})
        else:
            return json.dumps({'status': 400, 'message': 'Error fetching likes count'})

    except Exception as e:
        return json.dumps({'status': 500, 'message': f'Error: {str(e)}'})
#info per post 
@app.route('/getpost.info', methods=['POST','GET'])
def api_get_info_per_post(): 
    id_post = request.form.get('id_post')
    response = supabase.table('POST').select("*").eq('id', id_post).execute()  
    return json.dumps({'status':200,'message':'Post uploaded','data':response.data})


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
            "created_at":datetime.now().isoformat()
        }).execute()
            return json.dumps({'status': 200, 'message': 'Request sent', 'data': response.data})
        except Exception as e:
            return json.dumps({'status': 500, 'message': 'Error sending user request', 'error': str(e)})

    return json.dumps({'status': 500, 'message': error})

@app.route('/product.requests.per.user', methods=['GET', 'POST'])
def api_requests_count():
    try:
        id_user = request.form.get('id_user')
        response = supabase.table('Bookings').select('*').eq('user_id', id_user).execute()
        return json.dumps({'status': 200, 'message': 'Requests per user fetched', 'data': response.data})
    except Exception as e:
        return json.dumps({'status': 500, 'message': 'Error fetching requests ', 'error': str(e)})

#sarah
@app.route('/api', methods=["GET"])
def hello():
    return "It works!"
@app.route('/searchbycategory', methods=["POST"])
def search():
    query = request.args.get('query', '').strip()

    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    response_category = supabase.from_('categories').select('id').ilike('Category', f'%{query}%').execute()
    category = response_category.data if response_category else ""
   
    cats =[]
    for cat in category: 
        post_cat = supabase.from_('POST').select('id').eq('category_id', cat).execute()
        post_categories = post_cat.data if post_cat else ""
        cats.append(post_categories)

    response_data = {        
        'category': cats,
    }

    return jsonify(response_data)

@app.route('/searchbylocation', methods=["POST"])
def searchbylocation():
    query = request.args.get('query', '').strip()
    price = request.args.get('price', '').strip()
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400
    
    response_location = supabase.from_('POST').select('id').ilike('location', f'%{query}%').lte('price', price).execute()
    location = response_location.data if response_location else ""

    reponse_data = {
        'location': location,
        }
    return reponse_data


@app.route('/searchbyusers', methods=["POST"])
def searchbyusers():
    query = request.args.get('query', '').strip()

    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400
    
    response_user = supabase.from_('USERS').select('*').ilike('fullname', f'%{query}%').execute()
    users = response_user.data if response_user else ""
   
    return users



@app.route('/searchbydescription', methods=["POST"])
def searchbydescription():
    query = request.args.get('query', '').strip()
    price = request.args.get('price', '').strip()
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400
    
    response_description = supabase.from_('POST').select('id').ilike('Description', f'%{query}%').lte('price', price).execute()
    description = response_description.data if response_description else ""
    
    return description


@app.route('/getpost', methods=['POST'])
def getPost():
    query = request.args.get('query', '').strip()
    post = supabase.from_('POST').select('*').eq('id', query).execute()
    post_info = post.data if post else ""
    return post_info


@app.route('/getcategories', methods=['GET'])
def getCategory():
    categories = supabase.from_('categories').select('Category').execute()
    categories = categories.data if categories else ""
    return categories


@app.route('/getdesc', methods=['POST'])
def getDesc():
    query = request.args.get('query', '').strip()
    price = request.args.get('price', '').strip()
    desc = supabase.from_('POST').select('Description').lte('price',price).ilike('Description',f'%{query}%').execute()
    descritpions = desc.data if desc else ""
    return descritpions

@app.route('/getloc', methods=['POST'])
def getLoc():
    query = request.args.get('query', '').strip()
    price = request.args.get('price', '').strip()
    desc = supabase.from_('POST').select('location').lte('price',price).ilike('location',f'%{query}%').execute()
    descritpions = desc.data if desc else ""
    return descritpions


@app.route('/getcategory', methods=['POST'])
def getcategory():
    query = request.args.get('query', '').strip()
    desc = supabase.from_('categories').select('Category').ilike('Category',f'%{query}%').execute()
    descritpions = desc.data if desc else ""
    return descritpions

###############################user bio #####################################
@app.route('/getUserBio', methods=['POST'])
def GetBio(): 
    query = request.args.get('id', '').strip()
    bio = supabase.from_('USERS').select('Bio').eq('id',query).execute()
    bio = bio.data if bio else ""
    return bio[0]['Bio']
###########################Update user profile #############################

@app.route('/UpdateUserInfo', methods=['POST'])
def update(): 
    id= request.args.get('id', '').strip()
    bio = request.args.get('bio', '').strip()
    fullname = request.args.get('fullname', '').strip()

    resposne = supabase.table('USERS').update({'fullname':fullname, 'Bio':bio}).eq('id', id).execute()
    if(resposne): 
        dt = jsonify({'message': 200})
        return dt
    else: 
        dt = jsonify({"message":404})
        return dt


@app.route('/GetPostBookingsIds', methods=['POST'])
def BookingIds(): 
    query= request.args.get('query', '').strip()
    
    response = supabase.from_('Bookings').select('post_id','status').eq('user_id',query).neq('status','completed').execute()
    reponsedecoding = response.data if response else ""
    return reponsedecoding


@app.route('/GetHistoryBookings',methods=['POST'])
def history(): 
    query= request.args.get('query', '').strip()
    response = supabase.from_('Bookings').select('post_id','status').eq('user_id',query).neq('status','pending').execute()
    reponsedecoding = response.data if response else ""
    return reponsedecoding

@app.route('/')
def about():
    return 'Welcome ENSIA Students'

