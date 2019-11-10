# API Reference

1. [Register](#register)
2. [Login](#login)
3. [Logout](#logout)
4. [Profile](#profile)
5. [Edit Profile](#edit-profile)
6. [Post Ads](#post-ads)
7. [Ads Info](#ads-info)
8. [Ads Listing](#ads-listing)
9. [Log](#log)



### Register

![](https://img.shields.io/badge/POST-register-orange)

```
https://chotot-recommendersys.appspot.com/register
```

**Request Headers:**
- Content-Type: application/json

**Query Parameters:**

| Fields | Type | Required |
| --- | --- | --- |
| phone | String | x |
| password | String | x |

**Example:**
```json
{
    "phone": "123456789",
    "password": "AlicePassword"
}
```

**Response 200:** Successfully create a new account.
```json
{
    "status": 200,
    "message": "Successfully registered"
}
```

### Login

![](https://img.shields.io/badge/POST-login-orange)
```
https://chotot-recommendersys.appspot.com/login
```

**Request Headers:**
- Content-Type: application/json

**Query Parameters:**

| Fields | Type | Required |
| --- | --- | --- |
| phone | String | x |
| password | String | x |

**Example:**
```json
{
    "phone": "123456789",
    "password": "AlicePassword"
}
```

**Response 200:** If successfully logged in, return access token.
```json
{
    "status": 200,
    "access_token": "<access_token>"
}
```

### Logout
![](https://img.shields.io/badge/DELETE-logout-purple)
```
https://chotot-recommendersys.appspot.com/logout
```

**Request Headers:**
- Content-Type: application/json
- Authorization: Bearer <access_token>

**Response 200:** Successfully logged out.
```json
{
    "status": 200,
    "message": "Successfully logged out"
}
```

### Profile
![](https://img.shields.io/badge/GET-profile-green)
```
https://chotot-recommendersys.appspot.com/user/personal-profile
```

**Request Headers:**
- Content-Type: application/json
- Bearer Token: <access_token>

**Response 200:** Return user profile.
```json
{
    "status": 200,
    "profile": {
        "phone": "123456789",
        "name": "Alice",
        "birth_date": {
            "day": 4,
            "month": 10,
            "year": 2000
        },
        "gender": "other",
        "email": "alice@xyz.com",
        "region": "Alice's place",
        "area": "Alice's location"
    }
}
```


### Edit Profile
![](https://img.shields.io/badge/PUT-edit-blue)
```
https://chotot-recommendersys.appspot.com/user/edit
```

**Request Headers:**
- Content-Type: application/json
- Bearer Token: <access_token>

**Query Parameters:**

| Fields | Type | Required |
| --- | --- | --- |
| name | String, not null | |
| gender | Enum ('male', 'female', 'other') | |
| birth_date | {"day": \<day>, "month": \<month>, "year": \<year>} | |
| address | String | |
| email | String | |


**Example:**
```json
{
    "name": "Alice",
    "gender": "female",
    "birth_date": {
        "day": 4,
        "month": 10,
        "year": 2000
    },
    "email": "alice@xyz.com"
    "region_id": 1,
    "area_id": 3
}
```

**Response 200:** Successfuly updated user profile.
```json
{
    "status": 200,
    "message": "Successfully updated profile"
}
```


### Post Ads
![](https://img.shields.io/badge/POST-post-orange)
```
https://chotot-recommendersys.appspot.com/post)
```

**Request Headers:**
- Content-Type: application/json
- Bearer Token: <access_token>

**Query Parameters:**

| Fields | Type | Required |
| --- | --- | --- |
| main\_category_id | Integer | x |
| category_id | Integer | x |
| seller_type | Enum ('pro', 'active') | x |
| adtype | Enum('sell', 'rent', 'let') | x |
| subject | String | x |
| price | Integer | x |
| content | String | x |
| number\_of_img | Integer | x |
| image_url | String | x |
| thumbnail\_img_url | String | x |
| region_id | Integer | x |
| area_id | Integer | x |

**Params:**


**Example:**
```json
{
    "basics": 
    {
        "subject": "Mobile ABC",
        "price": 5000000,
        "main_category_id": 5,
        "category_id": 5010,
        "seller_type": "pro",
        "adtype": "sell",
        "content": "Need to sell mobile ABC.",
        "area_id": 402001, 
        "region_id": 4020,
        "image_url": null, 
        "number_of_img": 0,
        "thumbnail_img_url": null
    },
    "parameters":
    {
        "mobile_type": 1,
        "condition_ad": 1,
        "mobile_brand": 1,
        "mobile_color": 3,
        "mobile_model": 7,
        "elt_condition": 2,
        "mobile_capacity": 3
    }
}
```

**Response 200:** Successfully upload a new post.
```json
{
    "status": 200,
    "message": "Successfully posted"
}
```

### Ads Info
![](https://img.shields.io/badge/GET-infor-green)
```
https://chotot-recommendersys.appspot.com/info
```

**Request Headers:**
- Content-Type: application/json

**Query Params:**

| Key | Data Type |
| --- | --- |
| adlist_id | Integer |

**Example:**
```
https://chotot-recommendersys.appspot.com/info?adlist_id=1
```

**Response 200:** Return ad infor.
```json
{
    "infor": {
        "area_name": "area xyz",
        "category_name": "Phone",
        "content": "Need to sell mobile ABC.",
        "date": "2019-09-25T14:06:52",
        "is_sticky": false,
        "main_category_name": "Tech",
        "number_of_img": 0,
        "parameters": {
            "laptop_screen_size": "9 - 10.9 inch",
            "pc_driver_capacity": "256 GB",
            "pc_vga": "Onboard"
        },
        "price_str": "5000000",
        "publisher": {
            "area_id": null,
            "avatar": null,
            "id": 1,
            "name": "user",
            "phone": "Alice's phone",
            "region_id": null
        },
        "region_name": "region xyz",
        "seller_type": "pro",
        "subject": "Mobile ABC",
        "thumbnail_img_url": null
    },
    "status": 200
}
```



### Ads Listing
![](https://img.shields.io/badge/GET-adlisting-green)
```
https://chotot-recommendersys.appspot.com/adlisting)
```

**Request Headers:**
- Content-Type: application/json

**Query Params:**

| Key | Data Type |
| --- | --- |
| main_category | Integer |
| category | Integer |
| max_price | Integer |
| min_price | Integer |
| seller_type | Enum('pro', 'active') |
| region | Integer |
| area | Integer |

**Example:**
```
https://chotot-recommendersys.appspot.com/adlisting?main_category=5&category_id=5003&min_price=2000000&seller_type=pro
```

**Response 200:** Return list of ads summary.
```json
{
    "list_ad_infor": [
    {
        "area": "Area abc",
        "category_name": "Mobile",
        "is_sticky": false,
        "main_category_name": "Tech",
        "number_of_img": 0,
        "price_str": "12000000",
        "publisher":
        {
            "area": "Area xyz",
            "avatar": "Avatar Link",
            "id": 1,
            "name": "Alice",
            "phone": "Alice's Phone",
            "region": "Region xyz"
        },
        "region": "Region abc",
        "seller_type": "pro",
        "subject": "Need to sell mobile ABC.",
        "thumbnail_img_url": null
    }
    ],
    "status": 200
}
```

### Log
![](https://img.shields.io/badge/POST-logging-create)
```
https://chotot-recommendersys.appspot.com/logging/create)
```

**Request Headers:**
- Content-Type: application/json

**Query Parameters:**

| Fields | Type | Required |
| --- | --- | --- |
| adlist_id | Integer | x |
| ad_placement | Enum('default', 'top', 'bottom') | x |
| ad_position | Positive Integer | x |
| user_fingerprint | String | x |
| event\_client_time | String | x |
| page_name | Enum('ADLISTING', 'ADVIEW') | x |
| page_number | Positive Integer | x |
| page_device | Enum('DESKTOP', 'HANDY') | x |
| filter_brand | Integer | x |
| filter\_main\_category_id | Integer | x |
| filter\_category_id | Integer | x |
| filter_keyword | Integer | x |
| filter_price | String | x |
| filter\_region_id | Integer | x |
| filter\_area_id | Integer | x |
| filter_adtype | Enum('sell', 'buy', 'let', 'rent') | x |

**Example:**

```json
{
    "adlist_id": 1,
    "ad_placement": "top",
    "ad_position": 2,
    "ad_source": "stickyad",
    "user_fingerprint": "9fsdasfdasdfas",
    "event_client_time": "2019-09-26T22:30:12",
    "event_server_time": "2019-09-26T22:31:00",
    "page_name": "ADLISTING",
    "page_number": 1,
    "page_device": "HANDY",
    "filter_brand": null,
    "filter_main_category_id": null,
    "filter_category_id": null, 
    "filter_keyword": null,
    "filter_price": "1200000-3000000",
    "filter_region_id": 13000,
    "filter_area_id": null,
    "filter_adtype": null
}
```

**Response 200:** Successfully logged to database
```json
{
    "status": 200,
    "message": "Successfully logged"
}
```