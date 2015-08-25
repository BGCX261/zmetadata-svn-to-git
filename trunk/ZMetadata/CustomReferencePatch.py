from Products.Archetypes import config
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.Field import Field,ObjectField

def get(self, instance, aslist=False, mimetype=None, **kwargs):
    """get() returns the list of objects referenced under the relationship
    """    
    res=instance.getBRefs(relationship=self.relationship)
    res+=instance.getRefs(relationship=self.relationship)
    if mimetype == "text/plain":
        return ' '.join([obj.Title() for obj in res])
        if not self.multiValued and not aslist:
            if res:
                pass
 #               assert len(res) == 1
            res=res[0]
        else:
            res=None
        return res
#        assert type([]) == type(res)
    return res

def set(self, instance, value, **kwargs):    
    """Mutator.
    ``value`` is a list of UIDs or one UID string to which I will add a
    reference to. None and [] are equal.
    Keyword arguments may be passed directly to addReference(), thereby
    creating properties on the reference objects.
    """    
    tool = getToolByName(instance, "reference_catalog")
    backtargetUIDs = [ref.sourceUID for ref in
                     tool.getBackReferences(instance, self.relationship)]
    targetUIDs = [ref.targetUID for ref in
                 tool.getReferences(instance, self.relationship)]

    if not self.multiValued and value and type(value) not in (type(()),type([])):
        value = (value,)

    if not value:
        value = ()
    
    uids=[]
    for v in value:
        if type(v) in (type(''),type(u'')):
            uids.append(v)
        else:
            uids.append(v.UID())

    toobj = lambda uid: tool.lookupObject(uid)
    add = [toobj(v) for v in uids if v and v not in targetUIDs + backtargetUIDs]
    sub = [toobj(t) for t in targetUIDs if t not in uids]
    backsub = [toobj(t) for t in backtargetUIDs if t not in uids]
    
    toreindex = []
    
    addRef_kw = kwargs.copy()
    addRef_kw.setdefault('referenceClass', self.referenceClass)
    if addRef_kw.has_key('schema'): del addRef_kw['schema']

        
    for obj in add:
        __traceback_info__ = (instance, obj.UID(), value, targetUIDs)        
        if addRef_kw.get('isBackReference', None):
            src,tgt = obj, instance.UID()
        else:
            tgt,src = obj, instance.UID()
        tool.addReference(src, tgt, self.relationship, **addRef_kw)

    for obj in sub:
        tool.deleteReference(instance.UID(), obj, self.relationship)
    for obj in backsub:
        tool.deleteReference(obj, instance.UID(), self.relationship)

    if self.callStorageOnSet:        
        ObjectField.set(self, instance, self.getRaw(instance), **kwargs)

    for obj in sub + backsub + add:
        obj.reindexObject() 
        
        
def getRaw(self, instance, aslist=False, **kwargs):
    """Return the list of UIDs referenced under this fields
    relationship
    """
    rc = getToolByName(instance, "reference_catalog")
    brains = rc(targetUID=instance.UID(),
                relationship=self.relationship)
    res = [b.sourceUID for b in brains]
    brains = rc(sourceUID=instance.UID(),
                relationship=self.relationship)
    res += [b.targetUID for b in brains]
    
    if not self.multiValued and not aslist:
        if res:
            res = res[0]
        else:
            res = None
    return res      

 