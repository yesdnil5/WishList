function change(ranid, item){
	new Mongo();
	db = connect("localhost:27017/test");
	db.testData.update(
			{"id" : ranid, "Item" : item},
			{ "bought": true });
}
