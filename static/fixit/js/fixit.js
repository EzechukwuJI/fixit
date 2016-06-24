<script>
	$('body').on('change', '#stateinput', function(){
		var state      = $('#stateinput').find(':selected').attr('value');
		var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
		function csrfSafeMethod(method){
			// these HTTP methods do not require CSRF protection
			return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		$.ajaxSetup({
			beforeSend: function(xhr, settings){
				if (!csrfSafeMethod(settings.type) && !this.crossDomain){
					xhr.setRequestHeader("X-CSRFToken", csrf_token);
				}
			}
		});
		$.ajax({
			url: "{% url 'fixitMain:createjob' %}",
			type: "POST",
			data: {selected_state: state, csrfmiddlewaretoken: csrf_token, fieldname: "state" },
			success: function(data){
				$('#areainput').html(data);
				$('#areainput').prop('readonly',false);
			},
			error: function(data){
				$('#areainput').html('<option value="nothing">error occured </option>');	
			}
		})
}) 

var country_states =  [
	['Nigeria', ['Abia','Adamawa','Akwa-Ibom','Anambra','Bauchi','Benue','Borno',
	    'Cross-River','Delta','Edo','Enugu','Lagos', 'Katsina']],
	    ['Ghana',['accra','kumasi']] 
	]

$('body').on('change', '#countryinput', function(){
	var states = "";
	var selected_country = $('#countryinput').find(':selected').attr('value');
	for (var country in country_states ){
		if (country_states[country][0] === selected_country ){
			states = country_states[country][1];
		}
	}
	$('#stateinput').html("");
	for (var state in states ){
		$('#stateinput').append('<option value=' + states[state] + '>' + states[state] + '</option>');
	}
})

<script>
	$('body').on('change', '#stateinput', function(){
		var state      = $('#stateinput').find(':selected').attr('value');
		var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
		function csrfSafeMethod(method){
			// these HTTP methods do not require CSRF protection
			return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		$.ajaxSetup({
			beforeSend: function(xhr, settings){
				if (!csrfSafeMethod(settings.type) && !this.crossDomain){
					xhr.setRequestHeader("X-CSRFToken", csrf_token);
				}
			}
		});
		$.ajax({
			url: "{% url 'fixitMain:createjob' %}",
			type: "POST",
			data: {selected_state: state, csrfmiddlewaretoken: csrf_token, fieldname: "state" },
			success: function(data){
				$('#areainput').html(data);
				$('#areainput').prop('readonly',false);
			},
			error: function(data){
				$('#areainput').html('<option value="nothing">error occured </option>');	
			}
		})
}) 

var country_states =  [
	['Nigeria', ['Abia','Adamawa','Akwa-Ibom','Anambra','Bauchi','Benue','Borno',
	    'Cross-River','Delta','Edo','Enugu','Lagos', 'Katsina']],
	    ['Ghana',['accra','kumasi']] 
	]

$('body').on('change', '#countryinput', function(){
	var states = "";
	var selected_country = $('#countryinput').find(':selected').attr('value');
	for (var country in country_states ){
		if (country_states[country][0] === selected_country ){
			states = country_states[country][1];
		}
	}
	$('#stateinput').html("");
	for (var state in states ){
		$('#stateinput').append('<option value=' + states[state] + '>' + states[state] + '</option>');
	}
})
</script>