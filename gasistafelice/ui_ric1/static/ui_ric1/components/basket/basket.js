app.controller("BasketController", function ($http, $rootScope, parsingNumbers, productManager) {

    this.pm = productManager;
    this.gm = $rootScope.gm;
    this.dataLoaded = true;

    this.sorting = ''; //basket table sorting name
    this.reverseSort = false; //basket table sorting
    this.tbd_sorting = ''; //basket to be delivered table sorting name
    this.tbd_reverseSort = false; //basket to be delivered table sorting

    this.open_ordered_products = [];
    this.closed_ordered_products = [];
    var THAT = this;


    this.get_ordered_products_from_basket = function(basket) {
        var products = [];
        angular.forEach(basket, function(gmo, index) {
            var gsop = gmo.ordered_product;
            var min_amount = parsingNumbers.parsing(gsop.stock.detail_minimum_amount);
            var step_unit = parsingNumbers.parsing(gsop.stock.detail_step);
            var order_state = gsop.order.current_state.toLowerCase();

            products.push({
                id : gsop.id,
                price : parsingNumbers.parsing(gmo.ordered_price),
                quantity: parsingNumbers.parsing(gmo.ordered_amount),
                note : gmo.note,
                name : gsop.stock.product.__unicode__,
                supplier : gsop.order.supplier,
                order_shortname : "Ord. " + gsop.order.id,
                can_update : order_state == "open",
                order_state : order_state,
                step : step_unit,
                min_amount : min_amount
            });
        });
        return products;
    };

    $http.get($rootScope.absurl_api+'gasmember/' + $rootScope.gm_id+'/?format=json')
    .success(function(data) {

        $rootScope.gm = data;
        var gm = $rootScope.gm;
        console.debug("Recuperato il paniere per " + gm.id);

        THAT.open_ordered_products = THAT.get_ordered_products_from_basket(gm.basket);
        THAT.closed_ordered_products = THAT.get_ordered_products_from_basket(gm.basket_to_be_delivered);

    }).error(function(data){
        alert("http error get GAS member data");
    });

    return;
});

/*
 * app.controller("BasketController", function ($http, $rootScope, $sce, ngDialog, $modal, person, parsingNumbers) {
    
$scope.btbd = [];
$scope.orderByField = '';
$scope.reverseSort = false;
    
var order = "";
var suppliername = "";
var productname = "";
var ordprice = "";
var ordamount = "";
$scope.amount = [];
$scope.basket = [];
$scope.basket_post = [];
$scope.basket_2 = [];
$scope.basket_empty = "true";
var index = 1;
var value = "";
$scope.path=$.absurl_pre+"rest/gasmember/"+ $rootScope.gasmemberID+"/basket/edit_multiple";

//use $rootScope.gasmemberID to get the right JSON
    
$scope.dataLoaded = "false";
$scope.prodnumber = 0;
    
// NEW CODE
var gm = person.selected_gasmember;
$.each(gm.basket_to_be_delivered, function(i, el) {
    var price = parsingNumbers.parsing(el.ordered_product.order_price);
    var amount = parsingNumbers.parsing(el.ordered_amount);
    var detail_step = parsingNumbers.parsing(el.ordered_product.stock.detail_step);
    var detail_minimum_amount = el.ordered_product.stock.detail_minimum_amount;
    $scope.basket.push({
        id: el.ordered_product.id,
        order: el.order.substring(0, el.order.indexOf(' ',2)),
        supplier: el.supplier,
        gm: gm.id,
        product: el.product,
        price: price,
        amount: amount,
        total: amount*price,
        step: detail_step,
        minimum: detail_minimum_amount,
        delete: "false"
    });

      //LOADING POST basket data
      $scope.basket_post.push({
            id: basket[0].substring(0,5),
            gm_id: $rootScope.gasmemberID,
            gsop_id: b.ordered_product.id,
            ordered_price: parsingNumbers.parsing(basket[4].substring(13,8)),
            ordered_amount: parsingNumbers.parsing($scope.amount[i])
      });
});

//END NEW CODE
//
//$http.get($.absurl_pre+'rest/gasmember/'+$rootScope.gasmemberID+'/basket/edit_multiple?render_as=table&iDisplayLength=-1').success(function(data){
//      $.each(data.aaData, function(index, basket){
//          value = basket[6].indexOf("value");
//          step = basket[6].indexOf("step");
//          if ($.isNumeric(basket[6].substr(value+7,2)))
//          {
//            index = 2;
//            amount = basket[6].substr(value+7,2);
//          }
//          else{
//            amount = basket[6].substr(value+7,1);
//          }
//          //LOADING basket data
//          $http.get($.absurl_api+'gasmember/'+$rootScope.gasmemberID+'/?format=json').
//          success(function(item){
//              $.each(item.basket, function(i,b){
//                 if (b.id == basket[0].substring(0,5))
//                 {
//                     
//                 }
//              });
//          });
//          
//          $scope.basket.push({
//			id: basket[0].substring(0,5),
//                        order: basket[1],
//                        supplier: basket[2],
//			            gm: $rootScope.gasmemberID,
//                        price: parseFloat(basket[4].substring(13,8)),
//                        amount: parseFloat(amount),
//                        total: amount * parseFloat(basket[4].substring(13,8)),
//                        step: parseFloat(basket[6].substr(step+6,1)),
//                        delete: "false"});
//          
//          //LOADING POST basket data
//          $scope.basket_post.push({
//			id: basket[0].substring(0,5),
//			            gm: $rootScope.gasmemberID,
//                        price: parseFloat(basket[4].substring(13,8)),
//                        amount: parseFloat(amount)
//          });
//          
//          $scope.prodnumber = $scope.prodnumber + 1;
//      });
//	$scope.dataLoaded = "true";
// });      
//    
    
var i = 0;
    

    
$scope.getData = function(){
    
/*$http.get($.absurl_pre+'rest/gasmember/'+$rootScope.gasmemberID+'/basket/edit_multiple?render_as=table&iDisplayLength=-1').success(function(data){
    $scope.basket_2 = data;
    console.log($scope.basket_2.aaData);
    if ($scope.basket_2.aaData === "") {
            $scope.basket_empty = "false";
    }
    $.each(data.aaData, function(index, basket){
          
          value = basket[6].indexOf("value");
          step = basket[6].indexOf("step");
          if ($.isNumeric(basket[6].substr(value+7,2)))
          {
            index = 2;
            $scope.amount[i] = basket[6].substr(value+7,2);
          }
          else{
            $scope.amount[i] = basket[6].substr(value+7,1);
          }
          
          i = i + 1;
         
          //LOADING basket data
          
          
        $http.get($.absurl_api+'gasmember/'+$rootScope.gasmemberID+'/?format=json').
          success(function(item){
              i = 0;
              $.each(item.basket, function(i,b){
                 if (b.id == basket[0].substring(0,5)) {
                        bp = basket[4].substring(13,8);
                        bp = bp.replace(",", "."); 
                        $scope.basket.push({
                            id: b.ordered_product.id,
                            order: basket[1],
                            supplier: basket[2],
                            gm: $rootScope.gasmemberID,
                            product: basket[3],
                            //price: parsingNumbers.parsing(basket[4].substring(13,8)),
                            price: parsingNumbers.parsing(bp),
                            amount: parsingNumbers.parsing($scope.amount[i]),
                            //total: $scope.amount[i] * parsingNumbers.parsing(basket[4].substring(13,8)),
                            total: $scope.amount[i] * parsingNumbers.parsing(bp),
                            step: parsingNumbers.parsing(basket[6].substr(step+6,1)),
                            delete: "false"
                        });

                      //LOADING POST basket data
                      $scope.basket_post.push({
                            id: basket[0].substring(0,5),
                            gm_id: $rootScope.gasmemberID,
                            gsop_id: b.ordered_product.id,
                            ordered_price: parsingNumbers.parsing(basket[4].substring(13,8)),
                            ordered_amount: parsingNumbers.parsing($scope.amount[i])
                      });
                      
                      $scope.prodnumber = $scope.prodnumber + 1;
                     i = i + 1;
                }
             });
          });
      });
	$scope.dataLoaded = "true";
    console.log($scope.basket_post);
 });finecommento// 
};

$scope.getData();
    
//BTBD getting data
/*$http.get('./lib/gasmemberNEW.json').success(function(data){
      $.each(data.basket_to_be_delivered, function(index, basket){
            order = basket.ordered_product.order;
            suppliername = basket.supplier.name;
            productname = basket.ordered_product.gasstock.stock.product.name;
            ordprice = basket.ordered_price;
            ordamount = basket.ordered_amount;
            total = ordprice * ordamount;
            $scope.btbd.push({order_id: order,
                              supplier: suppliername,
                              product: productname,
                              price: ordprice,
                              amount: ordamount,
                              total: total});
      });
 });finecommento//

$scope.toggleSelection = function toggleSelection(i) {
    
    if ($scope.basket_post[i].enabled == true)
    {
        $scope.basket_post[i].enabled = false;
    }
    else{
        $scope.basket_post[i].enabled = true;
    }
    
};

$scope.delete = function ( idx ) {
  var person_to_delete = $scope.basket[idx];
  $scope.basket.splice(idx, 1);
  $scope.basket_post.splice(idx, 1);
};   
    
     $scope.increment = function(product,i){
        quantity = parsingNumbers.parsing(product.amount);
        quantity += product.step;
        product.amount = quantity;
        product.total = quantity * product.price;
        $scope.basket_post[i].ordered_amount += product.step;
        //console.log($scope.products_post[i].ordered_amount);
    }
    
    $scope.change = function(product,i){
        quantity = parsingNumbers.parsing(product.amount);
        product.total = quantity * product.price;
        $scope.basket_post[i].ordered_amount = quantity;
        //console.log($scope.products_post[i].ordered_amount);
    }
    
        $scope.decrement = function(product,i){
        quantity = parsingNumbers.parsing(product.amount, 10);
        console.log(quantity);
        sum = quantity - product.step;
        console.log(sum);
        if (sum > -1) {
            product.amount -= product.step;
            $scope.basket_post[i].ordered_amount -= product.step;
            product.total = product.amount * product.price;
        }
        }
    
    $scope.getTotal = function(){
    var total = 0;
    for(var i = 0; i < $scope.basket.length; i++){
        var product = $scope.basket[i];
        total += product.total;
    }
    return parseFloat(total).toFixed(2);
}
 
      
$scope.elimina = function(){   
}  

$scope.open = function (size) {

    var modalInstance = $modal.open({
      templateUrl: 'myModalContent.html',
      size: size
    });
}

$scope.close = function()
{
    var modalInstance = $modal.close();
}




    $scope.addtoCart = function($modalInstance){
            $scope.basket_post.push({TOTAL_FORMS:$scope.prodnumber,
                                       INITIAL_FORMS:0,
                                        MAX_NUM_FORMS:""});
            /*ngDialog.open({ template: 'popupTemplate',
                            className: 'ngdialog-theme-flat',
                            scope: $scope}); finecommentostar//
            $http.post($scope.path, {form:$scope.basket_post})
            .success(function(){
                $scope.basket_post.splice($scope.basket_post.length - 1 , 1);  
                $scope.basket = [];
                $scope.basket_post = [];
                $scope.getData();
                alert("Paniere aggiornato!");
            })
            .error(function(){
                $scope.basket_post.splice($scope.basket_post.length - 1, 1);   
                alert("Qualcosa è andato storto, riprova!");
            });
    }
    
    $scope.clickToOpen = function () {
           
    };
       

}



function FrmPaniereController($scope,$http,transformRequestAsFormPost){
                
}


paniereController.resolve = {
    r_gasmemberID : function($q, $http, $routeParams, $route, $rootScope) {
        var deferred = $q.defer();
        $http.get($.absurl_api+'person/'+ $rootScope.peID +'/?format=json')
            .success(function(data) {
                $rootScope.gasID = data.gas_list[0].id;
                $rootScope.gasmemberID = data.gasmembers[0];
                deferred.resolve(data)
            })
            .error(function(data){
                deferred.resolve("error value");
            });

        return deferred.promise;
    }
};
*/
