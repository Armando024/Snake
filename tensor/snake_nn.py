import tensorflow as tf
import pandas as pd

def load_data(path="../train_data/test0.csv"):#sepearting inputs and expected outputs
    train=pd.read_csv(path,names=['left','right','up','down','distance','chosen'],header=0)
    inputs,outs=train,train.pop('chosen')
    #outs=train.pop('chosen')
    #print(inputs)
    #print(outs)
    
    return inputs,outs

def train_input(features,labels,batch_size): #turns training data into tensor objects to train my model
   # print(features)
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)
    return dataset

def eval_input(features,labels,batch_size):
    features=dict(features)
    if labels is None:
        inputs=features
    else:
        inputs=(features,labels)

    dataset=tf.data.Dataset.from_tensor_slices(inputs)

    assert batch_size is not None, "wrong, batch must be none"
    dataset=dataset.batch(batch_size)
    
    return dataset

def main(argv):
    #fetch training data
    inputs,outs=load_data()

    test_inputs,test_outs=load_data("train.csv")    
    #features
    features=[]
    for key in inputs.keys():
        #print(key)
        features.append(tf.feature_column.numeric_column(key=key))
   # print(features)  
    
    model=tf.estimator.DNNClassifier(feature_columns=features,model_dir="snake_nn",hidden_units=[25],n_classes=4)
    
    model.train(input_fn=lambda:train_input(inputs,outs,100),steps=100000)
    
   #next step is to test my model
    eval_result=model.evaluate( input_fn=lambda:eval_input( test_inputs,test_outs,100))

    print('\nTest accuracy: {accuracy:0.3f}\n'.format(**eval_result))
     
    #see u in the next file lol
    
if __name__=='__main__':
    tf.app.run(main)








