function create(name) {
  $.get( "https://api.pi-dns.me/v1/stable/create", { name: name} , function( data ) {
    alert( "Status Code: " + data.statusCode + "\n" +
            "Response: " + data.response
            );
  });
}
