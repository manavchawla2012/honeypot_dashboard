function lpuEnc(value){
  var enOBJ = new JSEncrypt();
  enOBJ.setPublicKey($('pubkey').value);
  return enOBJ.encrypt(value);
}