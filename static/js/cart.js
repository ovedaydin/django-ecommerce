var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i< updateBtns.length; i++ ){
  updateBtns[i].addEventListener('click', async function(){
    console.log(this.dataset.product)
    var productId = this.dataset.product
    var action = this.dataset.action
    console.log('productId:',productId,'action:',action)
    console.log('USER:',user)
    document.getElementsByClassName('addToCart')[0].classList.add("hidden")
    document.getElementsByClassName('loader')[0].classList.remove("hidden")
    if(user == 'AnonymousUser'){
      await addCookieItem(productId, action)
      await updateUserOrder(productId, action)

    }else{
      await updateUserOrder(productId, action)

    }
    document.getElementsByClassName('addToCart')[0].classList.remove("hidden")
    document.getElementsByClassName('loader')[0].classList.add("hidden")


  })

}

async function addCookieItem(productId, action){
  console.log('Not logged in')
  if (action == 'add'){
    if(cart[productId] == undefined){
      cart[productId] = {'quantity':1}
    }else{
      cart[productId]['quantity'] += 1
    }
  }
  if (action == 'remove'){
    cart[productId]['quantity'] -= 1
    if (cart[productId]['quantity'] <= 0){
      console.log('Remove Item')
      delete cart[productId]
    }
  }
  await console.log('Cart:', cart)
  document.cookie = 'cart=' + JSON.stringify(cart)+ ";domain=;path=/"
  //location.reload()


  updateCartData()
}

async function updateUserOrder(productId, action){
  console.log('User logged in, sending data...')
  var url = '/update_item/'

  await fetch(url,{
    method:'POST',
    headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken,},
    body: JSON.stringify({'productId': productId, 'action':action})

  } )

  .then((response) =>{
    return response.json()
  } )


  .then((data) =>{
    console.log('data:', data)
    //location.reload()

  } )

  updateCartData()
}

function updateCartData(){
  var url = '/api/cartItems/'

  fetch(url,{
    method:'GET',
    headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken,},

  } )

  .then((response) =>{
    return response.json()
  } )


  .then((data) =>{
    console.log('data:', data)
    document.getElementById('cart-index').innerText = 'Sepet (' + data +')'
  } )
}


var updateBundles = document.getElementsByClassName('update-bundle')
var limit =  Number(document.getElementById('limit'))

for(var i = 0; i< updateBundles.length; i++ ){
  updateBundles[i].addEventListener('click',function(){
    console.log(this.dataset.product)
    var productId = this.dataset.product
    var action = this.dataset.action
    updateBundle(productId,action)

  })

}

function updateBundle (productId, action){
  var quantity = document.getElementById(productId)
  var number = Number(quantity.innerText)
  if (action == 'add'){
      number += 1
  }
  if (action == 'remove'){
    number -= 1
    if (number <= 0){
      number = 0
    }
  }
  quantity.innerText = number
}
