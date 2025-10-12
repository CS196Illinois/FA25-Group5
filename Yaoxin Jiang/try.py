int findRMP(string profName) {
    string [] nameParts = profName.split(",").strip()
    string firstName = nameParts[1].strip()
    string lastName = nameParts[0].strip()
    #rating = get RMP rating with web crawler with url: "https://www.ratemyprofessors.com/search/professors/1112?q=$String $String", Firstname, lastname
    if (profExist) {
        return rating
    }
    else {
        return -1
    }
}