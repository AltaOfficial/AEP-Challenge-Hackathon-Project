import tensorflow as tf
from transformers import TFAutoModelForCausalLM, AutoTokenizer
from datasets import Dataset


def finetune_llama_tf(train_data, val_data):
    """Fine-tune the LLaMA 3.2 model on the safety comment data using TensorFlow."""
    # Load pre-trained LLaMA 3.2 model and tokenizer
    model_name = "meta-llama/Llama-2-7b-hf"  # Adjust as needed for LLaMA 3.2
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = TFAutoModelForCausalLM.from_pretrained(model_name)

    # Tokenize the data
    def tokenize_function(examples):
        return tokenizer(examples["input"], truncation=True, padding="max_length", max_length=512)

    train_dataset = Dataset.from_dict({"input": [item["input"] for item in train_data]})
    val_dataset = Dataset.from_dict({"input": [item["input"] for item in val_data]})

    tokenized_train = train_dataset.map(tokenize_function, batched=True)
    tokenized_val = val_dataset.map(tokenize_function, batched=True)

    # Convert to TensorFlow datasets
    tf_train_dataset = model.prepare_tf_dataset(
        tokenized_train,
        shuffle=True,
        batch_size=4
    )
    tf_val_dataset = model.prepare_tf_dataset(
        tokenized_val,
        shuffle=False,
        batch_size=4
    )

    # Compile the model
    optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
    model.compile(optimizer=optimizer)

    # Fine-tune the model
    model.fit(
        tf_train_dataset,
        validation_data=tf_val_dataset,
        epochs=3
    )

    return model, tokenizer


if __name__ == "__main__":
    train_data, val_data, _ = prepare_data()  # Assuming prepare_data() is available
    fine_tuned_model, tokenizer = finetune_llama_tf(train_data, val_data)

    # Save the fine-tuned model
    fine_tuned_model.save_pretrained("./fine_tuned_llama_tf")
    tokenizer.save_pretrained("./fine_tuned_llama_tf")