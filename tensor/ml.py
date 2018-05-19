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
    print(features)
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)
    return dataset

def eval_input(features,labels,batch_size):
    features=dict(features)
    if label is None:
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
        
    #features
    features=[]
    for key in inputs.keys():
        print(key)
        features.append(tf.feature_column.numeric_column(key=key))
    print(features)  
    
    model=tf.estimator.DNNClassifier(feature_columns=features,model_dir="model1",hidden_units=[25],n_classes=4)
    
    model.train(input_fn=lambda:train_input(inputs,outs,100),steps=100000)
    
   #how would i evaluate this mode? hummmmmm....
   #next step is to test my model
    #see u in the next file lol
     
    
if __name__=='__main__':
    tf.app.run(main)








