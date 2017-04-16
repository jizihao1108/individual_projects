class SentNeuralNetwork:
    def __init__(self, reviews, labels, hidden_nodes = 10, learning_rate = 0.1):
        
        np.random.seed(1)
        
        self.preprocessing(reviews, labels)
        
        print(len(self.word2index))
        
        self.init_NeuralNet(len(self.review_list), hidden_nodes, 1, learning_rate)
    def preprocessing(self, reviews, labels):
        
        # add all the words to the set
        review_set = set()
        for review in reviews:
            for word in re.sub(r'[^\w]', ' ', review).split(' '):
                review_set.add(word)
                
        # add convert the set to the list
        self.review_list = list(review_set)
        
        # add labels to the set
        label_set = set()
        for label in labels:
            label_set.add(label)
            
        # convert the set to the list
        self.label_list = list(label_set)
        
        # calcualte the length of vocab size and label size
        self.review_size = len(self.review_list)
        self.label_size = len(self.label_list)
        
        # create dict to map word to specific index
        self.word2index = {}
        for index, word in enumerate(self.review_list):
            self.word2index[word] = index
        
        # create dict to map label to specific index
        self.label2index = {}
        for index, word in enumerate(self.label_list):
            self.label2index[word] = index
        
    def init_NeuralNet(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        
        # Initialize number of nodes
        self.input_nodes = input_nodes
        self.output_nodes = output_nodes
        self.hidden_nodes = hidden_nodes
        
        # Initialize the rate of learning
        self.learning_rate = learning_rate
        
        # Initialize the weight
        #self.weight_0_1 = np.random.normal(0.0, self.hidden_nodes**-.5, (self.input_nodes, self.hidden_nodes))
        self.weight_0_1 = np.zeros((self.input_nodes, self.hidden_nodes))
        self.weight_1_2 = np.random.normal(0.0, self.hidden_nodes**-.5, (self.hidden_nodes, self.output_nodes))
        
        # Initialize the input layer
        self.layer_0 = np.zeros((1, self.input_nodes))
        
    def update_input(self, review):
        self.layer_0 *= 0
        
        for word in re.sub(r'[^\w]', ' ', review).split(' '):
            if (word in self.word2index.keys()):
                self.layer_0[0][self.word2index[word]] = 1
    
    def get_target_for_label(self, label):
        
        if (label == 'POSITIVE'):
            return 1
        else:
            return 0
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self,x):
        return x * (1 - x)
    
    def train(self, training_reviews, training_labels):
        
        assert(len(training_reviews) == len(training_labels))
        
        # Remember the start time
        start_time = time.time()
        
        correct_counts = 0
        
        for i in range(len(training_reviews)):
            
            # update the input layer
            self.update_input(training_reviews[i])
            
            # get hidden layer by multiplying layer0 with weight_0_1
            lay_1 = np.dot(self.layer_0, self.weight_0_1)
            
            # get output layer by multiplying layer1 with weight_1_2
            lay_2 = np.dot(lay_1, self.weight_1_2)
            lay_2_out = self.sigmoid(lay_2)
            
            # get the real label value
            y = self.get_target_for_label(training_labels[i])
            
            # Calculate the output error
            err2 = y - lay_2_out
            err2_term = err2 * self.sigmoid_derivative(lay_2_out)
            
            # Calculate the hidden layer error
            err1 = np.dot(err2_term, self.weight_1_2.T)
            err1_term = err1
            
            # update weight_1_2
            self.weight_1_2 += np.dot(lay_1.T, err2_term) * self.learning_rate
            self.weight_0_1 += np.dot(self.layer_0.T, err1_term) * self.learning_rate
        
            # Check the training result
            if (lay_2_out > 0.5 and y == 1):
                correct_counts += 1
            elif (lay_2_out < 0.5 and y == 0):
                correct_counts += 1
                
            gone_time = time.time() - start_time
            reviews_per_second = i / gone_time if gone_time > 0 else 0
            
            sys.stdout.write("\rProgress:" + str(100 * i/float(len(training_reviews)))[:4] \
                             + "% Speed(reviews/sec):" + str(reviews_per_second)[0:5] \
                             + " #Correct:" + str(correct_counts) + " #Trained:" + str(i+1) \
                             + " Training Accuracy:" + str(correct_counts * 100 / float(i+1))[:4] + "%")
            if(i % 2500 == 0):
                print("")
