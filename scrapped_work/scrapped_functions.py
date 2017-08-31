def summarize(token_dict, cos):
    '''
    Returns the average cosine similarity for the documents in each folder.
    ex: client_folder = summarize(token_dict, cos)
    '''
    client_folder = OrderedDict()
    num_client_folder = 0
    total_num_docs = 0
    # goes through all the folders
    for key in token_dict.keys():
        cos_sum = 0
        avg_cos = 0
        num_docs = 0
        # goes through all the documents in each folder
        for doc_num in xrange(len(token_dict[key])):
            cos_sum += cos[total_num_docs] # might be wrong
            num_docs += 1
            total_num_docs += 1
        # avg_cos would be 0 for folders that are empty
        if num_docs > 0:
            avg_cos = cos_sum / num_docs
        client_folder[num_client_folder] = avg_cos
        num_client_folder += 1
    return client_folder


def categorize(token_dict, client_folder, categories):
    '''
    Returns the cosine similarity of a new document to each category
    ex: result = categorize(token_dict, client_folder, categories)
    '''
    result = {}
    # goes through each category
    for category in categories:
        category_avg = 0
        num_folders = 0
        # goes through all the folders
        for folder in token_dict.keys():
            # gets all the folders of a particular category
            if category == folder.split('-')[2]:
                if type(client_folder[int(folder.split('-')[0])]) != int:
                    category_avg += client_folder[int(folder.split('-')[0])][0]
                    num_folders += 1
        category_avg = category_avg / num_folders
        result[category] = category_avg
    return result


def predict(result):
    prediction = ''
    similarity = 0
    for key, value in result.iteritems():
        if value > similarity:
            similarity = value
            prediction = key
    return prediction


def predictions(result):
    lst = []
    for k, v in result.iteritems():
        lst.append((v, k))
    lst.sort(reverse=True)
    # decides the confidence interval you would want to accept
    if lst[0][0] > 2 * lst[1][0]:
        return lst[0][1]
    else:
        return lst[:3]
