function create() {
  subdomain = $("#subdomain").val();
  $.get( "https://api.pi-dns.me/v1/stable/create", { name: subdomain} , function( data ) {
    alert( "Status Code: " + data.statusCode + "\n" +
            "Response: " + data.response
            );
  });
}
