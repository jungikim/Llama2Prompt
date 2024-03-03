
class Util():
  @staticmethod
  def _getEntriesFromTable(text, ignore_header=True, num_fields=2):
    retVal=[]
    headerIgnored=(not ignore_header)
    for l in text.split('\n'):
      if l.startswith('|'):
        if headerIgnored:
          l = l.strip('| ').rstrip(' |')
          f = l.split(' | ')
          if num_fields == 1:
            retVal.append(tuple(' | '.join(f)))
          elif num_fields == 2:
            retVal.append(tuple([f[0], ' | '.join(f[1:])]))
          elif num_fields >= 3:
            if len(f) != num_fields:
              while len(f) < num_fields:
                f.append(' ')
              if len(f) > num_fields:
                f = f[:num_fields]
            retVal.append(tuple(f))
        headerIgnored=True
    return retVal

  # generate_words() and build_prompt() are from https://github.com/OpenNMT/CTranslate2/blob/master/examples/llama2/chat.py
  @staticmethod
  def generate_words(sp, step_results):
    tokens_buffer = []
    for step_result in step_results:
      is_new_word = step_result.token.startswith("▁")
      if is_new_word and tokens_buffer:
        word = sp.decode(tokens_buffer)
        if word:
          yield word
        tokens_buffer = []
      tokens_buffer.append(step_result.token_id)
    if tokens_buffer:
      word = sp.decode(tokens_buffer)
      if word:
        yield word

  @staticmethod
  def build_prompt(sp, dialog):
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
    if dialog[0]["role"] == "system":
      dialog = [
          {
              "role": dialog[1]["role"],
              "content": B_SYS + dialog[0]["content"] + E_SYS + dialog[1]["content"],
          }
      ] + dialog[2:]
    assert all([msg["role"] == "user" for msg in dialog[::2]]) and all(
      [msg["role"] == "assistant" for msg in dialog[1::2]]
    ), (
      "model only supports 'system', 'user' and 'assistant' roles, "
      "starting with 'system', then 'user' and alternating (u/a/u/a/u...)"
    )
    dialog_tokens = sum(
      [
        ["<s>"]
        + sp.encode_as_pieces(
            f"{B_INST} {(prompt['content']).strip()} {E_INST} {(answer['content']).strip()} "
        )
        + ["</s>"]
        for prompt, answer in zip(
            dialog[::2],
            dialog[1::2],
        )
      ],
      [],
    )
    assert (
      dialog[-1]["role"] == "user"
    ), f"Last message must be from user, got {dialog[-1]['role']}"

    dialog_tokens += ["<s>"] + sp.encode_as_pieces(
      f"{B_INST} {(dialog[-1]['content']).strip()} {E_INST}"
    )
    return dialog_tokens
