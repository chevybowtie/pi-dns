function create() {
  subdomain = $("#subdomain").val();
  $.get( "https://api.pi-dns.me/v1/stable/create", { name: subdomain} , function( data ) {
    alert( "Status Code: " + data.statusCode + "\n" +
            "Response: " + data.response
            );
  });
}
function update() {
  secret = $("#secret").val();
  name = $("#name").val();
  $.get( "https://api.pi-dns.me/v1/stable/update", { name: name, secret: secret} , function( data ) {
    alert( "Status Code: " + data.statusCode + "\n" +
            "Response: " + data.response
            );
  });
}
