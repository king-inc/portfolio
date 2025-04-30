:-set_prolog_flag(double_quotes, chars).


% Predicate to read a file into Prolog
read_file_to_string(File, String) :-
    open(File, read, Stream),
    read_stream_to_codes(Stream, Codes),
    close(Stream),
    atom_codes(String, Codes).

% Predicate to read and parse vCard file
read_and_parse_vcard_file(File, AST) :-
    read_file_to_string(File, FileContent),
		% remove end line chars and split vcard into list
    split_string(FileContent, '\n', '\n', PreprocessedFileContent),
		% parse vcard
		parse_vcard(PreprocessedFileContent,AST),
		vcard_to_html(AST, Html),
		open('output.html', write, Stream),
    write(Stream, Html),
    close(Stream).

% base case
parse_vcard([], []).
% pattern match list to take each property
parse_vcard([Prop|Props],AST):-
		% split property by ':' to make a key, value tuple
		split_prop(Prop,Tuple),
		% recurse on the remaining property
		parse_vcard(Props, Rest),
		% add parsed property to AST
		append([Tuple],Rest, AST).

% split property by ':' and then parse property 
split_prop(Prop, Out):-
		split_string(Prop,":","",Split),
		parse_prop(Split, Out).

% parse property to split multiple values for one key and keep ':' for certain values
parse_prop([],[]).
parse_prop([Head,Tail],Out):-
		split_string(Tail,";","",SplitTail),
		Out = (Head,SplitTail).
parse_prop([Head|Tail],Out):-
		concat_list(Tail, Concatted),
		Out = (Head,Concatted).

concat_list([X],Out):-
		string_concat(:, X, Out).
concat_list([Head|Tail],Out):-
		concat_list(Tail,Rest),
		string_concat(Head,Rest,Out).


% Convert vCard AST to HTML
vcard_to_html(Vcard, Html) :-
    html_header(Header),
    properties_to_html(Vcard, PropsHtml),
    html_footer(Footer),
    string_concat(Header, PropsHtml, TempHtml),
    string_concat(TempHtml, Footer, Html).

% Convert list of properties to HTML
properties_to_html([], '').
properties_to_html([(Name, Value)|Props], Html) :-
    format(atom(PropHtml), '<tr><td>~w:</td><td> ~w</td></tr>', [Name, Value]),
    properties_to_html(Props, RestHtml),
    string_concat(PropHtml, RestHtml, Html).




% HTML header
html_header('<!DOCTYPE html>
<html>
<head>
    <title>vCard to HTML</title>
</head>
<body>
<h1>vCard Data</h1>
<table>').

% HTML footer
html_footer('</table>
</body>
</html>').

	


