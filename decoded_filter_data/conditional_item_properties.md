# Item Properties

Nothing selected in the UI

```
1: {
  1: "Item Properties"
  2: 0
  3: 0xffff0000
  4: {
    1: 2
  }
  5: 1
}
```

```
1: {
  1: "Item Properties"
  2: 0
  3: 0xffff0000
  4: {
    1: 2
	4: 1             //None
  }
  5: 1
}
```

```
1: {
  1: "Item Properties"
  2: 0
  3: 0xffff0000
  4: {
    1: 2
	4: 4             //Ancestral        
  }
  5: 1
}
```

```
1: {
  1: "Item Properties"
  2: 0
  3: 0xffff0000
  4: {
    1: 2
    4: 5             //None+Ancestral
  }
  5: 1
}
```

## Notes

- Interesting that they aren't using a bit field like the rarity field, or maybe they are but not starting at 1
