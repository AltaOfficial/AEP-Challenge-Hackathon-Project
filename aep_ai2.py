import aep_ai, torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer


def finetune_llama(train_data, val_data):
    # Load pre-trained LLaMA 3.2 model and tokenizer
    model_name = "/llama3.2"  # Adjust as needed for LLaMA 3.2
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Tokenize the data
    def tokenize_function(examples):
        return tokenizer(examples["input"], truncation=True, padding="max_length", max_length=512)

    tokenized_train = tokenize_function(train_data)
    tokenized_val = tokenize_function(val_data)

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
    )

    # Create Trainer instance
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
    )

    # Fine-tune the model
    trainer.train()

    return model, tokenizer


if __name__ == "__main__":
    train_data, val_data, _ = prepare_data()  # Assuming prepare_data() is available
    fine_tuned_model, tokenizer = finetune_llama(train_data, val_data)

    # Save the fine-tuned model
    fine_tuned_model.save_pretrained("./fine_tuned_llama")
    tokenizer.save_pretrained("./fine_tuned_llama")


